import streamlit as st
from datetime import datetime
import json
import time

# Page configuration
st.set_page_config(
    page_title="Common Clipboard",
    page_icon="📋",
    layout="centered"
)

# Custom CSS for better appearance
st.markdown("""
    <style>
    .stTextArea [data-baseweb=base-input] {
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .code-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        font-family: monospace;
        margin: 10px 0;
        border: 1px solid #ddd;
    }
    .timestamp {
        font-size: 0.8em;
        color: #666;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'text_entries' not in st.session_state:
    st.session_state.text_entries = []

# Function to save entries
def save_entries():
    with open("clipboard_entries.json", "w") as f:
        json.dump(st.session_state.text_entries, f)

# Function to load entries
def load_entries():
    try:
        with open("clipboard_entries.json", "r") as f:
            st.session_state.text_entries = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        st.session_state.text_entries = []

# Load entries when the app starts
load_entries()

# Main app
st.title("📋 Common Clipboard")
st.markdown("Type text on one device and copy it from any other device")

# Text input section
with st.form("text_form"):
    user_text = st.text_area("Type your text here:", height=150, key="user_text")
    submitted = st.form_submit_button("Save to Shared Clipboard")

    if submitted and user_text:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.text_entries.insert(0, {
            "text": user_text,
            "time": timestamp
        })
        # Keep only the last 20 entries
        st.session_state.text_entries = st.session_state.text_entries[:20]
        save_entries()
        st.success("Text saved! Refresh other devices to see updates.")

# Display section
st.subheader("Shared Clipboard Contents")

if not st.session_state.text_entries:
    st.info("Clipboard is empty. Add some text above.")
else:
    latest_entry = st.session_state.text_entries[0]

    st.markdown("**Latest Entry:**")
    st.markdown(f'<div class="timestamp">Last updated: {latest_entry["time"]}</div>', unsafe_allow_html=True)
    st.code(latest_entry["text"], language="text")

    if st.button("Copy Latest Text"):
        st.code(latest_entry["text"], language="text")
        st.success("Text ready to copy from the box above!")

    # Show history (optional)
    with st.expander("View History (Last 20 entries)"):
        for i, entry in enumerate(st.session_state.text_entries[1:], 1):
            st.markdown(f"**Entry {i}** ({entry['time']})")
            st.code(entry["text"], language="text")

# Auto-refresh every 15 seconds
st.markdown("""
    <script>
    setTimeout(function(){
        window.location.reload(1);
    }, 15000);
    </script>
    """, unsafe_allow_html=True)
