END_POINT = "static.thuwy.top"
END_POINT_PORT = 443 # not used
FRONTEND_ORIGIN = "*"
TARGET_BUCKET = "image"
ACCESS_KEY = "access_key"
SECRET_KEY = "secret_key"
LISTEN_PORT = 5020

class FlaskConfig:
    UPLOAD_FOLDER = "/tmp/minio_upload"
    DEBUG=True