from os import chmod, environ, path as os_path
from subprocess import call as call_subprocess
from tempfile import NamedTemporaryFile


def generate_pdf(html='', url='', delete_html=True):
    # Validate input
    if not html and not url:
        raise ValueError('Must pass HTML or specify a URL')
    if html and url:
        raise ValueError('Must pass HTML or specify a URL, not both')

    wkhtmltopdf_default = os_path.join(
        os_path.split(os_path.split(os_path.abspath(__file__))[0])[0],
        'bin/wkhtmltopdf-heroku')

    # Reference command
    wkhtmltopdf_cmd = environ.get('WKHTMLTOPDF_CMD', wkhtmltopdf_default)

    # Set up return file
    pdf_file = NamedTemporaryFile(delete=False, suffix='.pdf')

    if html:
        # Save the HTML to a temp file
        html_file = NamedTemporaryFile(delete=delete_html, suffix='.html')
        html_file.write(bytes(html, encoding='utf-8'))
        # wkhtmltopdf
        call_subprocess([wkhtmltopdf_cmd, '-q', html_file.name, pdf_file.name])
        html_file.close()

    else:
        # wkhtmltopdf, using URL
        call_subprocess([wkhtmltopdf_cmd, '-q', url, pdf_file.name])

    return pdf_file
