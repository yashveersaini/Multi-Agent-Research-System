from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from langchain_tavily import TavilySearch
import os
from rich import print
from dotenv import load_dotenv

load_dotenv()

tavily = TavilySearch(max_results=5)


@tool
def web_search(query: str) -> dict:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs, and snippets."""
    
    results = tavily.invoke(query)  
    
    out = []

    for r in results.get('results', []):
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    return "\n------\n".join(out)


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        resp = requests.get(url, timeout=8, headers=headers)
        
        if resp.status_code != 200:
            return f"Failed to fetch page, status code: {resp.status_code}"

        soup = BeautifulSoup(resp.text, "html.parser")

        # safer version
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text[:3000] if text else "No readable content found."

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
    
