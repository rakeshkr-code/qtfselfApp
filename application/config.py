import os

basedir = os.path.abspath(os.path.dirname(__file__)) #get the current directory


class Config():
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    DEBUG = True


class HerokuConfig(Config):
    # SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "postgres://ktapjqmkfrtnxm:3c92b4b88806c0d3c507b1ff5f53290b8a3dfe43bd7c95112659552216d3b5ed@ec2-3-211-6-217.compute-1.amazonaws.com:5432/dffqka0nqma9oc"
    DEBUG = False
