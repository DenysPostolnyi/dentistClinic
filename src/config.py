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
    PASSWORD = os.getenv('MYSQL_PASSWORD')
    PORT = os.getenv('MYSQL_PORT')
    SQLALCHEMY_DATABASE_URL = "mysql+pymysql://" + USERNAME + ":" + PASSWORD + "@" + "0.0.0.0" + ":" + PORT + "/" + DATABASE