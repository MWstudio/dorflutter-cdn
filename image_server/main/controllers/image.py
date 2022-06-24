import os
from flask import (
    Blueprint,
    current_app,
    jsonify,
    request,
    send_from_directory
)
from flask_apispec import doc, use_kwargs
from werkzeug.utils import secure_filename
from image_server.main.schema import (
    RequestFileSchema
)

API_CATEGORY = "Image"
image_bp = Blueprint("image", __name__, url_prefix="/image")
app = current_app
path = os.path.abspath(app.config["IMAGE_FILE_PATH"])
port = app.config["PORT"]
host = app.config["HOST"]
base_dir = os.getcwd()


# debug 용도로 파일리스트 확인, 추후 삭제 예정
@image_bp.route("/", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="index",
    description="image server filelist"
)
def index():
  path = os.path.abspath(app.config["IMAGE_FILE_PATH"])    
  files = os.listdir(path)
  return jsonify(files)


@image_bp.route("/<path:path>", methods=["GET"])
@doc(
    tags=[API_CATEGORY],
    summary="donwload",
    description="image download"
)
def donwload(path):
  path_list = path.split('/')
  image_path = ''
  image_file = path_list[-1]
  
  for i in range(len(path_list)-1):
    image_path += '/'+path_list[i]
    
  abspath = os.path.abspath(app.config["IMAGE_FILE_PATH"])
  
  return send_from_directory(abspath + image_path, image_file)


@image_bp.route("/upload", methods=["POST"])
@doc(
    tags=[API_CATEGORY],
    summary="upload",
    description="image upload",
    consumes=["multipart/form-data"]
)
@use_kwargs(RequestFileSchema, location="files")
def upload(file):
  full_path = os.path.join(path, secure_filename(file.filename))
  file.save(full_path)
  return "success"


@image_bp.route("/delete", methods=['DELETE'])
def delete():
    filename = request.get_json()['filename']
    if filename != 'default.png':
      full_path = os.path.join(path, filename)
      os.remove(full_path)
    return "success"
    