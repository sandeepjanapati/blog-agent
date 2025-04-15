# AI Blog Writing Agent

## Overview

This project contains a Python-based autonomous agent designed to generate SEO-optimized blog posts. Given a topic, it researches using public APIs, writes content using Google Gemini, optimizes for SEO, and exports the results in Markdown and JSON formats.

Built for the Python Developer Role assessment, focusing on smart engineering principles like modularity, asynchronous operations, and API integration.

## Features

*   **Topic Analysis:** Breaks down the main topic into relevant subtopics.
*   **Contextual Research:** Uses NewsData.io (news), Datamuse (keywords), and Quotable.io (quotes).
*   **Content Generation:** Leverages Google Gemini API for introduction, body sections, and conclusion.
*   **SEO Optimization:** Generates title, meta description, tags, slug, estimated reading time, and Flesch-Kincaid readability score.
*   **Structured Output:** Exports blog content as `.md` and metadata as `.json`.
*   **Modular Design:** Code separated into distinct 'agent' responsibilities.
*   **Asynchronous Research:** Uses `asyncio` and `aiohttp` for concurrent API calls during research.
*   **Caching:** Uses `functools.lru_cache` for Datamuse API calls.
*   **Configurable Tone:** Use the `--tone` flag to influence writing style.
*   **CLI Interface:** Uses `argparse` for easy command-line execution.
*   **Environment Variable Management:** Uses `.env` for API keys via `python-dotenv`.

## Setup

1.  **Clone the repository (if applicable):**
    ```bash
    git clone <your-repo-url>
    cd blog_agent
    ```
2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API Keys:**
    *   Create a file named `.env` in the project root directory (`blog_agent/`).
    *   Add your API keys to the `.env` file:
        ```dotenv
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
        NEWSDATA_API_KEY=YOUR_NEWSDATA_API_KEY_HERE
        ```
    *   Replace the placeholders with your actual keys obtained from Google AI Studio and NewsData.io.

## Running the Agent

Execute the main script from the terminal:

```bash
python main.py --topic "Your Blog Post Topic Here"
```
Optional Arguments:
--tone: Specify the writing style (e.g., educational, creative, formal). Defaults to informative.
--output-dir: Set a custom directory for saving output files. Defaults to output/.
Example:
python main.py --topic "The Future of Artificial Intelligence" --tone "technical" --output-dir "generated_blogs"
Use code with caution.
Bash
Output
The agent will create a subdirectory within the specified output directory (or output/ by default). The subdirectory name will be the generated URL slug. Inside this folder, you will find:
<slug>.md: The full blog post content in Markdown format.
metadata.json: A JSON file containing the title, meta description, tags, slug, reading time, and readability score.

## Project Structure
```text
blog_agent/
├── agents/             # Core agent modules
│   ├── __init__.py
│   ├── understanding_agent.py
│   ├── research_agent.py
│   ├── writing_agent.py
│   ├── seo_agent.py
│   └── export_agent.py
├── utils/              # Helper functions and API clients
│   ├── __init__.py
│   └── api_clients.py
├── output/             # Default directory for generated blogs
├── venv/               # Virtual environment (ignored by git)
├── .env                # API Keys (ignored by git)
├── .gitignore          # Git ignore rules
├── main.py             # Main script orchestrator
├── README.md           # This file
└── requirements.txt    # Python dependencies
```
Use code with caution.
Evaluation Criteria Addressed
Content Quality: Structured Markdown, attempts SEO alignment via keywords/prompts.
API Integration: Uses Gemini, NewsData.io, Datamuse, Quotable.io purposefully.
Smart Engineering: Implements asyncio for research, lru_cache for Datamuse, modular design, basic error handling.
Reusability: Modular agents can potentially be reused or extended.
Output & UX: Exports .md and .json, provides CLI feedback via rich.
Bonus: Includes --tone flag and readability score calculation.