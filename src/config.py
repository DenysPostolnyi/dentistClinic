"""
File for creating config
"""
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv("../.env"))


class DBSettings:
    """
    class-config for DB
    """
    DATABASE = os.getenv('MYSQL_DATABASE')
    USERNAME = os.getenv('MYSQL_USERNAME')
    PASSWORD = os.getenv('MYSQL_PASSWORD') if os.getenv('MYSQL_PASSWORD') else ""
    HOST = os.getenv('MYSQL_HOST')
    PORT = os.getenv('MYSQL_PORT')
    if DATABASE is "db":
        SQLALCHEMY_DATABASE_URL = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + HOST + ":" + PORT + "/" + DATABASE
    elif DATABASE is "travis_db":
        SQLALCHEMY_DATABASE_URL = "mysql://" + USERNAME + ":" + PASSWORD + "@" + HOST + ":" + PORT + "/" + DATABASE
