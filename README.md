# AI Blog Writing Agent with Streamlit UI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://blogagent.streamlit.app/)

## Overview

This project is a Python-based autonomous agent designed to automate the process of generating SEO-optimized blog posts. Given a topic, it performs contextual research using public APIs, writes structured content using the Google Gemini API, optimizes it for search engines, and provides the output in both Markdown and JSON formats.

The agent features both a command-line interface (CLI) for direct execution and a user-friendly web interface built with Streamlit.

**Try the live application here:** 👉 **[https://blogagent.streamlit.app/](https://blogagent.streamlit.app/)** 👈

## Key Features

*   **Topic Analysis:** Breaks down the main topic into relevant subtopics using AI.
*   **Contextual Research:** Gathers background information using:
    *   **NewsData.io:** Fetches recent news articles related to the topic.
    *   **Datamuse API:** Finds semantic keyword variations for SEO.
    *   **Quotable.io:** Retrieves relevant quotes.
*   **AI Content Generation:** Leverages Google Gemini API (`gemini-1.0-pro`) for:
    *   Engaging introductions.
    *   Detailed sections based on subtopics.
    *   Strong conclusions with calls-to-action.
*   **SEO Optimization:** Generates:
    *   SEO-friendly Title.
    *   Meta Description (max 160 chars).
    *   Relevant Tags/Keywords.
    *   URL-friendly Slug.
    *   Estimated Reading Time.
    *   Flesch-Kincaid Readability Score (via `textstat`).
*   **Dual Interface:**
    *   **CLI:** Run the agent directly from the terminal (`main.py`).
    *   **Web UI:** Interactive Streamlit application (`app.py`) with input fields, tone selection, and history. Accessible live at [https://blogagent.streamlit.app/](https://blogagent.streamlit.app/).
*   **Structured Output:** Exports blog content as `.md` and metadata as `.json` in a structured output folder (when run locally or if file saving is enabled in deployment).
*   **Smart Engineering:**
    *   Modular design (separate agents for different tasks).
    *   Asynchronous API calls (`asyncio`, `aiohttp`) for research efficiency.
    *   Caching for Datamuse API results (`functools.lru_cache`).
    *   Configuration via `.env` (local) and Streamlit Secrets (deployment).
*   **Deployment Ready:** Deployed on Streamlit Cloud, using `st.secrets` for secure API key management.
*   **History Tracking:** The Streamlit UI keeps track of recently generated topics for easy reference and re-runs.

## Live Demo

Experience the AI Blog Agent live in your browser:

➡️ **[https://blogagent.streamlit.app/](https://blogagent.streamlit.app/)**

Simply enter a topic, choose a tone, and click "Generate Blog Post"!

## Technology Stack

*   **Core:** Python 3.8+
*   **AI Model:** Google Gemini API (`google-generativeai`)
*   **Web Framework (UI):** Streamlit (`streamlit`)
*   **HTTP Requests:** `requests` (sync), `aiohttp` (async)
*   **Configuration:** `python-dotenv` (local), Streamlit Secrets (deployed)
*   **CLI Enhancement:** `rich`
*   **Text Analysis:** `textstat`
*   **APIs Used:**
    *   Google Gemini API
    *   NewsData.io API
    *   Datamuse API
    *   Quotable.io API

## Running the Application

**1. Accessing the Deployed Web UI (Recommended):**

The easiest way to use the agent is via the deployed Streamlit application:

*   **URL:** [https://blogagent.streamlit.app/](https://blogagent.streamlit.app/)

**2. Running Locally (For Development/Modification):**

If you want to run the agent on your own machine:

*   **Setup:** Follow the steps in the "Setup (Local Development)" section below.
*   **Run Streamlit UI:**
    ```bash
    streamlit run app.py
    ```
    This will open the interface locally (usually at `http://localhost:8501`).
*   **Run Command-Line Interface (CLI):**
    ```bash
    python main.py --topic "Your Blog Post Topic Here" [--tone <tone>] [--output-dir <dir>]
    ```

## Setup (Local Development)

Follow these steps only if you intend to run the agent on your local machine:

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url> # Replace with your repo URL if different
    cd blog-agent
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
4.  **Configure Local API Keys:**
    *   Create a file named `.env` in the project root directory (`blog_agent/`).
    *   Add your API keys to the `.env` file. **Do not commit this file to Git.**
        ```dotenv
        # .env - For Local Development Only
        GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
        NEWSDATA_API_KEY=YOUR_NEWSDATA_API_KEY_HERE
        ```
    *   Replace the placeholders with your actual keys obtained from Google AI Studio and NewsData.io.

## Deployment (Streamlit Cloud)

This application is currently deployed on Streamlit Cloud. The deployment process involves:

1.  Pushing the code to a connected GitHub repository.
2.  Configuring API keys using Streamlit Cloud's **Secrets** management (Settings > Secrets) in TOML format:
    ```toml
    # .streamlit/secrets.toml - Format for Streamlit Cloud Secrets UI
    GEMINI_API_KEY = "YOUR_ACTUAL_GEMINI_API_KEY_HERE"
    NEWSDATA_API_KEY = "YOUR_ACTUAL_NEWSDATA_API_KEY_HERE"
    ```
3.  The code automatically checks `st.secrets` when deployed.

## Project Structure

```
blog_agent/
├── agents/             # Core agent modules (understanding, research, writing, etc.)
│   ├── __init__.py
│   ├── understanding_agent.py
│   ├── research_agent.py
│   ├── writing_agent.py
│   ├── seo_agent.py
│   └── export_agent.py
├── utils/              # Helper functions and API clients
│   ├── __init__.py
│   └── api_clients.py
├── output/             # Default directory for generated blogs (local runs)
├── venv/               # Virtual environment (ignored by git)
├── .streamlit/         # Streamlit configuration (secrets conceptually live here)
│   └── secrets.toml    # Example format - DO NOT COMMIT ACTUAL SECRETS
├── .env                # Local API Keys (ignored by git)
├── .gitignore          # Git ignore rules
├── app.py              # Streamlit application entry point
├── main.py             # CLI application entry point
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## Potential Improvements & Future Work

*   **Enhanced Error Handling:** Implement more specific error catching and robust retry logic (e.g., using `tenacity`).
*   **Unit & Integration Testing:** Add tests using `pytest` to ensure reliability.
*   **Advanced Prompt Engineering:** Experiment with different prompting techniques (personas, few-shot examples) for better content quality.
*   **Image Suggestions:** Add functionality to suggest relevant images or image search terms.
*   **Fact-Checking:** Integrate basic fact-checking mechanisms (challenging).
*   **Plagiarism Check:** Add an option to check generated content against external sources (likely requires paid APIs).
*   **More Sophisticated SEO:** Include internal linking suggestions, schema markup generation.
*   **Configuration File:** Use a `config.yaml` for more settings management.
*   **Direct CMS Publishing:** Add options to export/upload drafts to WordPress, Ghost, etc.