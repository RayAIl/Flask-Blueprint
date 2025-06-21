import os

class Config(object):
    APPNAME = 'app'
    ABSPATH_IN_APPNAME = os.path.abspath(APPNAME)
    UPLOAD_PATH = "/static/upload/"
    SERVER_PATH = ABSPATH_IN_APPNAME + UPLOAD_PATH

    USER = os.environ.get("POSTGRES_USER", 'postgres')
    PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'trazin')
    HOST = os.environ.get("POSTGRES_HOST", 'postgres')
    PORT = os.environ.get("POSTGRES_PORT", '5432')
    DB = os.environ.get("POSTGRES_DB", 'mydb')

    SQLALCHEMY_DATABASE_URI = f'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB}'
    SECRET_KEY = 'fdsfklgfd4skfpgo5kyonmv02i49g$_dsdft5[t0og4]'
    SQLALCHEMY_TRACK_MODIFICATIONS = True