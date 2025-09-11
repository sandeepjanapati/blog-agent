# app.py
import streamlit as st
import asyncio
import os
import datetime
from pathlib import Path

# Import the modified agent runner function
# Ensure VS Code/Python can find 'main' (running streamlit from root folder helps)
try:
    from main import run_blog_agent
except ImportError as e:
    st.error(f"Error importing agent function: {e}. Make sure you run streamlit from the project root directory.")
    st.stop() # Stop execution if import fails

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Blog Writing Agent",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Logo (Optional) ---
# Create a 'static' folder and put your logo there if you have one
# static_dir = Path(__file__).parent / "static"
# logo_path = static_dir / "logo.png"
# if logo_path.exists():
#     st.sidebar.image(str(logo_path), width=150)
# else:
st.sidebar.title("✍️ AI Blog Agent")


# --- Session State Initialization ---
if 'history' not in st.session_state:
    st.session_state.history = [] # List to store {'topic': str, 'tone': str, 'timestamp': str, 'slug': str}
if 'current_topic' not in st.session_state:
    st.session_state.current_topic = ""
if 'current_tone' not in st.session_state:
    st.session_state.current_tone = "informative"
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
if 'last_run_topic' not in st.session_state:
    st.session_state.last_run_topic = ""


# --- Helper Function to Run Agent ---
# This function will be called when the button is pressed
def trigger_agent_run():
    topic = st.session_state.current_topic
    tone = st.session_state.current_tone
    output_dir = "output" # Or make this configurable in UI

    if not topic:
        st.error("Please enter a topic.")
        return

    if st.session_state.is_running:
        st.warning("Agent is already running. Please wait.")
        return

    # Clear previous results before starting
    st.session_state.generated_content = None
    st.session_state.metadata = None
    st.session_state.is_running = True
    st.session_state.last_run_topic = topic # Store the topic being run

    # Use st.spinner for visual feedback
    with st.spinner(f"Generating blog post for '{topic}' with tone '{tone}'... Please wait."):
        try:
            # Run the async function using asyncio.run()
            # Pass run_mode='streamlit' to suppress CLI output and enable potential st messages
            markdown_content, metadata = asyncio.run(
                run_blog_agent(topic, tone, output_dir, run_mode='streamlit')
            )

            # Store results in session state
            st.session_state.generated_content = markdown_content
            st.session_state.metadata = metadata

            # Add to history if successful and topic is new
            if markdown_content and metadata:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                slug = metadata.get('slug', 'unknown-slug')
                # Avoid adding duplicates immediately
                if not any(h['topic'] == topic and h['tone'] == tone for h in st.session_state.history):
                     st.session_state.history.insert(0, { # Add to beginning
                         "topic": topic,
                         "tone": tone,
                         "timestamp": timestamp,
                         "slug": slug
                     })
                     # Limit history size (e.g., keep last 10)
                     st.session_state.history = st.session_state.history[:10]

                st.success("Blog post generated successfully!")
            else:
                # Error messages should be handled within run_blog_agent using st.error
                # But add a generic one here if it returns None without specific error
                if not st.session_state.generated_content and not st.session_state.metadata:
                     st.error("Blog post generation failed. Check logs or API keys.")


        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            # Log the full error for debugging if needed
            print(f"Streamlit App Error: {e}") # Print to console where streamlit runs
        finally:
            # Ensure the running flag is reset
            st.session_state.is_running = False
            # Rerun to update the UI elements based on the new state


# --- Sidebar Controls ---
st.sidebar.header("Configuration")

# Tone Selection
tone_options = ["informative", "educational", "creative", "formal", "technical", "beginner-friendly"]
st.session_state.current_tone = st.sidebar.selectbox(
    "Select Writing Tone:",
    options=tone_options,
    index=tone_options.index(st.session_state.current_tone) if st.session_state.current_tone in tone_options else 0,
    key='tone_selector' # Assign key for stability
)

st.sidebar.header("History")
if not st.session_state.history:
    st.sidebar.caption("No past topics yet.")
else:
    # Allow selecting a past topic to re-populate the input field
    history_topics = [f"{h['topic']} ({h['tone']}) - {h['timestamp']}" for h in st.session_state.history]
    selected_history = st.sidebar.radio(
        "Select a past topic to reload:",
        options=[""] + history_topics, # Add empty option to deselect
        index=0,
        key='history_selector'
    )

    if selected_history:
        # Find the corresponding history entry
        selected_index = history_topics.index(selected_history)
        history_entry = st.session_state.history[selected_index]
        # Update current topic and tone in session state
        st.session_state.current_topic = history_entry['topic']
        st.session_state.current_tone = history_entry['tone']
        # Clear the radio selection so it can be clicked again if needed
        # Setting the key directly might be more reliable for radio buttons
        st.session_state.history_selector = "" # Attempt to clear selection state

        # Use rerun to update the main input field immediately
        st.experimental_rerun() # OLD LINE



# --- Main Area ---
st.title("AI Blog Post Generator")
st.markdown("Enter a topic below and click 'Generate' to create a blog post.")

# Topic Input - Use session state to preserve value
st.text_input(
    "Blog Post Topic:",
    key='current_topic', # Bind to session state key
    placeholder="e.g., The Future of Renewable Energy",
    # Use on_change with a button press check, or rely solely on button
)

# Generate Button
st.button(
    "Generate Blog Post",
    on_click=trigger_agent_run,
    disabled=st.session_state.is_running, # Disable button while running
    type="primary" # Make button more prominent
)

# --- Display Results ---
st.markdown("---") # Separator
st.header("Generated Output")

if st.session_state.is_running and not st.session_state.generated_content:
     st.info(f"Processing topic: '{st.session_state.last_run_topic}'...") # Show which topic is running

elif st.session_state.generated_content:
    st.subheader("Blog Post Content (Markdown)")
    with st.expander("View/Hide Content", expanded=True):
        st.markdown(st.session_state.generated_content)

elif st.session_state.last_run_topic: # Show if run was attempted but failed before content generation
     st.warning(f"No content generated for the last run topic: '{st.session_state.last_run_topic}'. Check for errors above.")
else:
    st.info("Output will appear here after generation.")