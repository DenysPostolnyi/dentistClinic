"""
File for creating config
"""
import os
# from dotenv import load_dotenv, find_dotenv
#
# load_dotenv(dotenv_path=find_dotenv("../.env"))


class DBSettings:
    """
    class-config for DB
    """
    SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL')
