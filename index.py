import io

from flask import Flask, render_template, request, flash, redirect, url_for, make_response, Response, send_file
from werkzeug.utils import secure_filename
import os

from extractors.extract_mytaxi import parse_bill
from formatters.format_excel import format_excel

app = Flask(__name__)
app.config.update(
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
)

ALLOWED_EXTENSIONS = ['pdf']


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'files' not in request.files:
        flash('No file part')
        return redirect('/')

    pdfdocs = request.files.getlist('files')

    parseddocs = [parse_bill(file) for file in pdfdocs]
    excel = format_excel(parseddocs)
    response = send_file(io.BytesIO(excel), attachment_filename="parsed_invoices.xslx",
                         mimetype='application/xslx', as_attachment=True)

    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

    # TODO: set errors for wrong file, secure filenames, set filetype validation, set correct headers