from flask import Blueprint, request
import os
from werkzeug.utils import secure_filename
from image_processer import process_image

blueprint = Blueprint('routes', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@blueprint.route('/upload', methods=['POST'])
def upload_file():
    if 'image' in request.files:
        file = request.files['image']
        print(file)
        if file.filename == '' or not allowed_file(file.filename):
            return "Invalid or no file selected", 400
        else:
            # Call the process_image function and pass the file
            image_classification = process_image(file)
        return image_classification, 200
    return "No image found in request", 400