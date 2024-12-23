from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from transformers import pipeline
import requests
from bs4 import BeautifulSoup
import sqlite3
import os

app = FastAPI()

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "data.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scraped_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        content TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS processed_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT,
        result TEXT
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS combined_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        scraped_content TEXT,
        processed_result TEXT
    );
    """)
    conn.commit()
    conn.close()

init_db()

sentiment_analysis = pipeline("sentiment-analysis")

class ScrapeRequest(BaseModel):
    url: str

class ProcessRequest(BaseModel):
    text: str

class CombinedRequest(BaseModel):
    url: str

def get_db():
    conn = sqlite3.connect(DB_PATH)
    return conn

def scrape_website(url, cursor):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        titles = [title.get_text(strip=True) for title in soup.find_all("h1")]
        descriptions = [desc.get_text(strip=True) for desc in soup.find_all("p")]
        content = { "titles": titles, "descriptions": descriptions }

        cursor.execute("INSERT INTO scraped_data (url, content) VALUES (?, ?)", (url, str(content)))
        cursor.connection.commit()
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping website: {e}")

def process_text(text, cursor):
    try:
        result = sentiment_analysis(text)

        cursor.execute("INSERT INTO processed_data (text, result) VALUES (?, ?)", (text, str(result)))
        cursor.connection.commit()

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing text: {e}")

@app.post("/scrape")
def scrape_endpoint(request: ScrapeRequest, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    content = scrape_website(request.url, cursor)
    conn.commit()
    return { "url": request.url, "content": content }

@app.post("/process")
def process_endpoint(request: ProcessRequest, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    result = process_text(request.text, cursor)
    conn.commit()
    return { "text": request.text, "result": result }

@app.post("/combined")
def combined_endpoint(request: CombinedRequest, conn: sqlite3.Connection = Depends(get_db)):
    cursor = conn.cursor()
    content = scrape_website(request.url, cursor)
    result = process_text(content["descriptions"][0], cursor)
    cursor.execute("INSERT INTO combined_results (url, scraped_content, processed_result) VALUES (?, ?, ?)", (request.url, str(content), str(result)))
    conn.commit()
    return { "url": request.url, "scraped_content": content, "processed_result": result }