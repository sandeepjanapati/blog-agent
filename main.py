# main.py
import argparse
import os
import asyncio
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

# Import agent functions
from agents.understanding_agent import analyze_topic
from agents.research_agent import gather_research
from agents.writing_agent import generate_blog_post
from agents.seo_agent import generate_seo_metadata
from agents.export_agent import export_results

# Import utility functions
from utils.api_clients import get_gemini_client

# Initialize Rich Console
console = Console()

async def run_blog_agent(topic: str, tone: str, output_dir: str):
    """
    Main asynchronous function to run the blog writing agent workflow.
    """
    console.print(Panel(f"🚀 Starting Blog Agent for Topic: '[bold cyan]{topic}[/bold cyan]' | Tone: '[italic yellow]{tone}[/italic yellow]' 🚀", title="Blog Agent Initializing", border_style="blue"))

    # --- 0. Load Environment Variables & Initialize Clients ---
    load_dotenv() # Load API keys from .env file
    newsdata_api_key = os.getenv("NEWSDATA_API_KEY")
    if not newsdata_api_key:
        console.print("[bold red]Error: NEWSDATA_API_KEY not found in .env file.[/bold red]")
        return

    gemini_client = get_gemini_client() # Initialize Gemini client

    # --- 1. Understand the Topic ---
    analysis = analyze_topic(topic, tone, gemini_client)
    subtopics = analysis['subtopics']
    confirmed_tone = analysis['tone']
    console.print(f"   - Confirmed Tone: [italic yellow]{confirmed_tone}[/italic yellow]")
    console.print(f"   - Identified Subtopics: {subtopics}")


    # --- 2. Conduct Research (Async) ---
    research_data = await gather_research(topic, subtopics, newsdata_api_key)
    # console.print(f"   - Research Data Keys: {list(research_data.keys())}") # Optional: view keys


    # --- 3. Generate Content ---
    markdown_content = generate_blog_post(topic, subtopics, confirmed_tone, research_data, gemini_client)
    if len(markdown_content) < 100: # Basic check if content generation likely failed
         console.print("[bold red]Content generation seems to have failed or produced very short output. Exiting.[/bold red]")
         return


    # --- 4. SEO Optimization ---
    metadata = generate_seo_metadata(topic, markdown_content, research_data, gemini_client)
    console.print(f"   - Generated Title: [bold green]'{metadata['title']}'[/bold green]")
    console.print(f"   - Meta Description: '{metadata['meta_description']}'")
    console.print(f"   - Tags: {metadata['tags']}")
    console.print(f"   - Slug: '{metadata['slug']}'")
    console.print(f"   - Est. Reading Time: {metadata['reading_time_minutes']} min(s)")
    console.print(f"   - Readability (FK Grade): {metadata['readability_score']}")


    # --- 5. Export and Summarize ---
    md_path, json_path = export_results(markdown_content, metadata, output_dir, metadata['slug'])

    # --- Final Summary ---
    if md_path and json_path:
        summary_panel = Panel(
            f"✅ Blog post generation complete!\n\n"
            f"   - Topic: [bold cyan]{topic}[/bold cyan]\n"
            f"   - Output Directory: [bold magenta]{os.path.abspath(output_dir)}/{metadata['slug']}[/bold magenta]\n"
            f"   - Markdown File: [bold magenta]{md_path}[/bold magenta]\n"
            f"   - Metadata File: [bold magenta]{json_path}[/bold magenta]",
            title="Execution Summary",
            border_style="green"
        )
        console.print(summary_panel)
    else:
        console.print(Panel("❌ Blog post generation failed during export.", title="Execution Summary", border_style="red"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Python Blog Writing Agent")
    parser.add_argument("--topic", type=str, required=True, help="The main topic for the blog post.")
    parser.add_argument("--tone", type=str, default="informative", help="Desired writing tone (e.g., informative, educational, creative, formal).")
    parser.add_argument("--output-dir", type=str, default="output", help="Directory to save the generated files.")

    args = parser.parse_args()

    # Run the main async function
    try:
        asyncio.run(run_blog_agent(args.topic, args.tone, args.output_dir))
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred in the main execution: {e}[/bold red]")