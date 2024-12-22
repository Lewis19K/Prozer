from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
import sqlite3
import os

app = FastAPI()

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "data.db")
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


class ScrapeRequest(BaseModel):
    url: str

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        titles = [title.get_text(strip=True) for title in soup.find_all("h1")]
        descriptions = [desc.get_text(strip=True) for desc in soup.find_all("p")]
        return { "titles": titles, "descriptions": descriptions }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scraping website: {e}")

@app.post("/scrape")
def scrape_endpoint(request: ScrapeRequest):
    content = scrape_website(request.url)
    return { "url": request.url, "content": content }