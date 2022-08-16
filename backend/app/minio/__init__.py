from app import app
from flask import Blueprint, abort, make_response, request, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
from minio import Minio
from config import MinioConfig as config
from datetime import datetime, timedelta

from app.auth import requireScope

router = Blueprint("minio", __name__)
CORS(
    router,
    origins=config.FRONTEND_ORIGIN,
    supports_credentials=True
)

client = Minio(
    endpoint=config.END_POINT,
    access_key=config.ACCESS_KEY,
    secret_key=config.SECRET_KEY,
    secure=True
)

def makeDate():
    now = datetime.now()
    return f"""{now.year}/{now.strftime("%m")}/{now.day}"""


def timestamp():
    return int(datetime.now().timestamp() * 1000)


@router.route("/uploadurl")
@router.route("/uploadurl/<name>")
@requireScope(["User"])
def getUploadURL(name="unamed.bin"):
    filename = f"{makeDate()}/{timestamp()}_{name}"
    # print(f"filename: {filename}")

    try:
        url = client.presigned_put_object(
            config.TARGET_BUCKET,
            filename,
            expires=timedelta(days=1)
        )
        return {
            "code": 0,
            "msg": "OK",
            "data": url
        }
    except Exception as e:
        # print(e)
        abort(make_response({
            "code": 500,
            "msg": "failed",
            "exception": str(e)
        }, 500))


@router.route("/upload", methods=["POST"])
@router.route("/upload/<name>", methods=["POST"])
@requireScope(["User"])
def upload(name = None):
    if not request.files:
        abort(400)

    file = request.files["file"]
    # print(file)

    if file.filename == "":
        abort(400)


    originalName = secure_filename(file.filename)
    mimetype = file.mimetype
    filename = f"{makeDate()}/{timestamp()}_{name or originalName or 'unamed.bin'}"

    try:
        res = client.put_object(
            bucket_name=config.TARGET_BUCKET,
            object_name=filename,
            data=file.stream,
            content_type=mimetype,
            length=-1,
            part_size=10*1024*1024
        )

        # print("upload success, result" + str(res))
        return {"code": 0, "msg": "OK"}
    except Exception as e:
        # print(e)
        abort(make_response({
            "code": 500,
            "msg": "failed",
            "exception": str(e),
        }, 500))


if app.config.get("DEBUG"):
    @router.route("/testupload")
    def index():
        return send_file("minio/testupload.html")