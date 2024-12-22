from fastapi import FastAPI
import sqlite3
import os

app = FastAPI()

DB_PATH = "data.db"
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scraped_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    content TEXT
);
""")
conn.commit()