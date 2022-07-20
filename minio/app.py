from flask import Flask, abort, make_response, request, send_file
from werkzeug.utils import secure_filename
from flask_cors import CORS
from minio import Minio
from minio.api import ObjectWriteResult
import config
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(
    app,
    origins=config.FRONTEND_ORIGIN,
    supports_credentials=True
)


app.config.from_object(config.FlaskConfig)

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


@app.route("/uploadurl")
@app.route("/uploadurl/<name>")
def getUploadURL(name="unamed.bin"):
    filename = f"{makeDate()}/{timestamp()}_{name}"
    print(f"filename: {filename}")

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
        print(e)
        abort(make_response({
            "code": 500,
            "msg": "failed",
            "exception": str(e)
        }, 500))


@app.route("/upload", methods=["POST"])
@app.route("/upload/<name>", methods=["POST"])
def upload(name = None):
    if not request.files:
        abort(400)

    file = request.files["file"]
    print(file)

    if file.filename == "":
        abort(400)


    originalName = secure_filename(file.filename)
    mimetype = file.mimetype
    filename = f"{makeDate()}/{timestamp()}_{name or originalName or 'unamed.bin'}"

    try:
        etag: ObjectWriteResult = client.put_object(
            bucket_name=config.TARGET_BUCKET,
            object_name=filename,
            data=file.stream,
            content_type=mimetype,
            length=-1,
            part_size=10*1024*1024
        )

        print("upload success, etag" + str(etag))
        return {"code": 0, "msg": "OK"}
    except Exception as e:
        print(e)
        abort(make_response({
            "code": 500,
            "msg": "failed",
            "exception": str(e),
        }, 500))


if app.config.get("DEBUG"):
    @app.route("/")
    def index():
        return send_file("index.html")