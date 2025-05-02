import streamlit as st
import time
from datetime import datetime
import json
import uuid

# Page configuration
st.set_page_config(
page_title="Device-to-Device Copy Tool",
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
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'text_entries' not in st.session_state:
  st.session_state.text_entries = []
if 'room_id' not in st.session_state:
st.session_state.room_id = str(uuid.uuid4())[:8]

# Function to save entries
def save_entries():
with open(f"entries_{st.session_state.room_id}.json", "w") as f:
json.dump(st.session_state.text_entries, f)

# Function to load entries
def load_entries():
try:
with open(f"entries_{st.session_state.room_id}.json", "r") as f:
st.session_state.text_entries = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
st.session_state.text_entries = []

# Load entries when the app starts
load_entries()

# Main app
st.title("📋 Device-to-Device Copy Tool")
st.markdown("Type text on one device and copy it from another device using the same Room ID")

# Room ID section
col1, col2 = st.columns([3,1])
with col1:
new_room_id = st.text_input("Room ID", value=st.session_state.room_id)
with col2:
if st.button("Generate New Room"):
st.session_state.room_id = str(uuid.uuid4())[:8]
st.session_state.text_entries = []
save_entries()
st.experimental_rerun()

st.session_state.room_id = new_room_id

# Text input section
with st.form("text_form"):
user_text = st.text_area("Type your text here:", height=150)
submitted = st.form_submit_button("Save Text")

if submitted and user_text:
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.session_state.text_entries.insert(0, {
"text": user_text,
"time": timestamp
})
save_entries()
st.success("Text saved! Refresh other devices to see updates.")

# Display section
st.subheader("Saved Texts")
st.markdown(f"Room ID: `{st.session_state.room_id}` - Share this ID with other devices")

if not st.session_state.text_entries:
st.info("No texts saved yet. Add some text above.")
else:
for entry in st.session_state.text_entries:
with st.expander(f"📝 {entry['time']}"):
st.code(entry['text'], language="text")
if st.button("Copy", key=f"copy_{entry['time']}"):
st.code(entry['text'], language="text")
st.success("Text copied to clipboard! (Manually copy from the box above)")

# Auto-refresh every 30 seconds
st.markdown("""
<script>
setTimeout(function(){
window.location.reload(1);
}, 30000);
</script>
""", unsafe_allow_html=True)
