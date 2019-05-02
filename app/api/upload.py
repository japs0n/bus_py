from flask import request, jsonify, send_from_directory
from app.auth.authentication import auth
import os
from . import api
from config import config
import uuid


@api.route("/upload", methods=["POST"])
@auth.login_required
def upload():
    file = request.files.get('file', None)
    if file is None:
        return jsonify(error='未上传文件')
    if file.filename == '':
        return jsonify("未选择文件")
    random_filename = str(uuid.uuid4().hex) + '.' + file.filename.rsplit('.', 1)[1].lower()
    file.save(os.path.join(config['default'].UPLOAD_FOLDER, random_filename))
    return jsonify(error="0", url=config['default'].DOMAIN + '/upload/' + random_filename)


@api.route("/upload/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(config['default'].UPLOAD_FOLDER, filename)
