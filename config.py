from dotenv import load_dotenv
import os


class Database:
    def __init__(self):
        self.DB_HOST = os.environ.get("DB_HOST")
        self.DB_PORT = os.environ.get("DB_PORT")
        self.DB_NAME = os.environ.get("DB_NAME")
        self.DB_USER = os.environ.get("DB_USER")
        self.DB_PASS = os.environ.get("DB_PASS")
        self.url = f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


load_dotenv()
db = Database()