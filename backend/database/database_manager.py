import os
import mysql.connector
from dotenv import load_dotenv

# Get the current directory of this script
current_dir = os.path.dirname(os.path.realpath(__file__))
load_dotenv(os.path.join(current_dir, "../.env"))

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PSWD = os.getenv("DB_PSWD")
# DB_NAME = os.getenv("DB_NAME")

# Check if environment variables are loaded
if not DB_HOST or not DB_PORT or not DB_USER or not DB_PSWD:
    raise ValueError("Missing one or more environment variables (DB_HOST, DB_PORT, DB_USER, DB_PSWD)")

class DB:
    def __init__(self, host=DB_HOST, user=DB_USER, passwd=DB_PSWD, port=DB_PORT, db_name=None):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        self.db_name = db_name
        self.cursor = None
        self.db = None

    def db_info(self):
        if self.db:
            print(f"Connected to MySQL server at {self.db.server_host}")
            print(f"Database: {self.db_name}")
            print(f"Server version: {self.db.get_server_info()}")
            print(f"Protocol version: {self.db._protocol_version}")
            print(f"Server connection: {self.db.connection_id}")
            print(f"Server charset: {self.db.charset}")
            print(f"Server time zone: {self.db.time_zone}")
        else:
            print("No active database connection")

    def set_db_name(self, db_name):
        self.db_name = db_name

    def set_cursor_buffered_true(self):
        if self.db:
            self.cursor = self.db.cursor(buffered=True)

    def connect(self):
        try:
            self.db = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                port=self.port,
                database=self.db_name
            )
            self.cursor = self.db.cursor()
            if self.db.is_connected():
                print("Connected to the database")
            else:
                print("Failed to connect to the database")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.db = None

    def buffered_connect(self):
        self.connect()
        if self.db:
            self.set_cursor_buffered_true()

    def commit(self):
        if self.db:
            self.db.commit()

    def rollback(self):
        if self.db:
            self.db.rollback()
    
    def close(self):
        if self.db:
            self.db.close()

    def execute(self, operation, params=None, multi=False):
        if self.db:
            return self.cursor.execute(operation, params, multi)
        else:
            print("Database not connected")
            return None

    def fetchall(self):
        if self.db:
            return self.cursor.fetchall()
        else:
            print("Database not connected")
            return None

    def create_table(self, table_name, columns, primary_key=None, foreign_key=None):
        if self.db:
            query = f"CREATE TABLE {table_name} ({columns})"
            if primary_key:
                query += f", PRIMARY KEY ({primary_key})"
            if foreign_key:
                query += f", FOREIGN KEY ({foreign_key})"
            self.execute(query)
            self.commit()

    def drop_table(self, table_name):
        if self.db:
            self.execute(f"DROP TABLE {table_name}")
            self.commit()

    def select(self, table_name, columns, condition=None):
        if self.db:
            query = f"SELECT {columns} FROM {table_name}"
            if condition:
                query += f" WHERE {condition}"
            self.execute(query)
            return self.fetchall()
        return None
    
    def update(self, table_name, set_values, condition):
        if self.db:
            self.execute(f"UPDATE {table_name} SET {set_values} WHERE {condition}")
            self.commit()

    def insert(self, table_name, columns, values):
        if self.db:
            self.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({values})")
            self.commit()

    def delete(self, table_name, condition):
        if self.db:
            self.execute(f"DELETE FROM {table_name} WHERE {condition}")
            self.commit()
