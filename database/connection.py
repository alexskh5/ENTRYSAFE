import psycopg2
import json
import os
import traceback
from utils.paths import app_dir

class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            # base_path = os.path.dirname(__file__)
            base_path = app_dir()
            config_path = os.path.join(base_path, "config.json")

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file NOT found at {config_path}")

            with open(config_path, "r") as f:
                config = json.load(f)

            self.connection = psycopg2.connect(
                dbname=config["dbname"],
                user=config["user"],
                password=config["password"],
                host=config["host"],
                port=config["port"]
            )

            return self.connection

        except Exception:
            traceback.print_exc()
            return None

    def get_cursor(self):
        if self.connection is None:
            self.connect()
        return self.connection.cursor()
