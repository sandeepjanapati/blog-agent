# utils/api_clients.py
import os
import google.generativeai as genai
import requests
import aiohttp
import asyncio
import functools
from rich.console import Console

console = Console()

# --- Gemini Client ---
def get_gemini_client():
    """Initializes and returns the Gemini client."""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.0-flash')
        return model
    except Exception as e:
        console.print(f"[bold red]Error initializing Gemini client: {e}[/bold red]")
        return None

# --- NewsData.io Client ---
async def fetch_news_async(session, api_key, topic):
    """Fetches news related to the topic asynchronously."""
    # Basic URL encoding for the topic
    query = requests.utils.quote(topic)
    url = f"https://newsdata.io/api/1/news?apikey={api_key}&q={query}&language=en"
    # Add retry logic here later if needed
    try:
        async with session.get(url, timeout=15) as response: # Added timeout
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            data = await response.json()
            # Limit to top 3 relevant articles for context
            return data.get('results', [])[:3]
    except aiohttp.ClientError as e:
        console.print(f"[yellow]NewsData API request failed: {e}[/yellow]")
        return []
    except asyncio.TimeoutError:
        console.print("[yellow]NewsData API request timed out.[/yellow]")
        return []
    except Exception as e:
        console.print(f"[yellow]An unexpected error occurred during NewsData fetch: {e}[/yellow]")
        return []


# --- Datamuse Client ---
@functools.lru_cache(maxsize=128) # Cache results for repeated keyword lookups
def fetch_datamuse_keywords(topic):
    """Fetches related keywords from Datamuse."""
    keywords = set()
    try:
        # Means like
        response_ml = requests.get(f"https://api.datamuse.com/words?ml={topic}&max=10")
        response_ml.raise_for_status()
        keywords.update(item['word'] for item in response_ml.json())

        # Related triggers (often good for SEO)
        response_trg = requests.get(f"https://api.datamuse.com/words?rel_trg={topic}&max=10")
        response_trg.raise_for_status()
        keywords.update(item['word'] for item in response_trg.json())

        return list(keywords)[:15] # Limit total keywords
    except requests.exceptions.RequestException as e:
        console.print(f"[yellow]Datamuse API request failed: {e}[/yellow]")
        return []
    except Exception as e:
        console.print(f"[yellow]An unexpected error occurred during Datamuse fetch: {e}[/yellow]")
        return []

# --- Quotable.io Client ---
def fetch_quotable_quotes(topic_keywords):
    """Fetches quotes related to topic keywords."""
    quotes = []
    # Try fetching quotes for the first few keywords
    tags = "|".join(topic_keywords[:3]) # Search using OR for first 3 keywords
    if not tags:
        return []
    try:
        response = requests.get(f"https://api.quotable.io/quotes/random?limit=2&tags={tags}", timeout=10)
        response.raise_for_status()
        quotes_data = response.json()
        quotes = [f"\"{q['content']}\" - {q['author']}" for q in quotes_data]
        return quotes
    except requests.exceptions.RequestException as e:
        console.print(f"[yellow]Quotable API request failed: {e}[/yellow]")
        return []
    except Exception as e:
        console.print(f"[yellow]An unexpected error occurred during Quotable fetch: {e}[/yellow]")
        return []