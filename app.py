
# Streamlit app

import streamlit as st
from utils import get_video_id, get_transcript, get_video_title, format_transcript, detect_language
from summarizer import summarizer
from qa import qa_responder

import os
import yt_dlp

DEMO_MODE = True

# Initialize session state variables if they don't exist
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'transcript' not in st.session_state:
    st.session_state.transcript = None
if 'title' not in st.session_state:
    st.session_state.title = None
if 'video_id' not in st.session_state:
    st.session_state.video_id = None

st.set_page_config(page_title="YouTube Video Summarizer", page_icon="🎥", layout="centered")
st.title("🎥 YouTube Video Summarizer")

st.markdown("""
Welcome! This tool helps you quickly summarize any YouTube video using AI.

Paste a YouTube link below and get:
- A clean, human-readable summary
- Key bullet points with main ideas
- Ability to download your summary
- Ask custom questions about the video content

Great for learning faster, note-taking, or saving time!
""")

st.markdown("---")

url = st.text_input("Paste YouTube video link here:", placeholder="https://www.youtube.com/watch?v=abcd1234")

if st.button("Summarize Video"):
    if url.strip() == "":
        st.error("Please provide YouTube URL.")
    else:
        if DEMO_MODE:
            st.info("Running in Demo Mode: returning precoded responses.")
            # Set static demo values
            st.session_state.title = "Demo Video Title"
            st.session_state.video_id = "demo_video_id"
            st.session_state.transcript = (
                "This is a demo transcript simulating a YouTube video's content. "
                "It contains several sentences that mimic the structure and flow of a typical transcript."
            )
            st.session_state.summary = summarizer(st.session_state.transcript)
        else:
            try:
                # Use cookies.txt only if it exists
                cookie_path = "cookies.txt"
                use_cookies = os.path.exists(cookie_path)

                if use_cookies:
                    st.write("🔐 Cookies detected: True")
                else:
                    st.warning("No cookies.txt found. Only public videos may work.")

                ydl_opts = {'quiet': True}
                if use_cookies:
                    ydl_opts['cookiefile'] = cookie_path

                # Extract video info using yt_dlp
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                    st.success(f"Video found: {info.get('title', 'Unknown title')}")
                except yt_dlp.utils.DownloadError:
                    st.error("🚫 This video requires login (private/music/age-restricted). Try another public one.")
                    st.stop()
                
                with st.spinner("Fetching video title..."):
                    st.session_state.title = get_video_title(url)
                with st.spinner("Extracting video ID..."):
                    st.session_state.video_id = get_video_id(url)
                with st.spinner("Retrieving transcript..."):
                    st.session_state.transcript = get_transcript(st.session_state.video_id)
                if not st.session_state.transcript:
                    st.warning("Transcript not available for this video.")
                    st.session_state.summary = None
                else:
                    with st.spinner("Generating summary..."):
                        st.session_state.summary = summarizer(st.session_state.transcript)
            
            except ValueError as e:
                st.error(f"Error: {e}")
            
            except Exception as e:
                st.error(f"Something went wrong: {type(e).__name__} - {e}")


if st.session_state.summary:
    st.markdown(f"## 🎬 *{st.session_state.title}*")
    st.markdown("### ✨ Summary")
    st.text_area("Summary", st.session_state.summary, height=250)
    
    # if st.button("📋 Copy summary to clipboard"):
    #     st.toast("Summary copied! (Use Ctrl+C / Cmd+C to copy from the box above)")
    
    st.markdown("### 💬 Ask a question about this summary")
    user_question = st.text_input("Your question:")
    if st.button("Ask"):
        if user_question.strip() == "":
            st.warning("Please enter a question.")
        else:
            with st.spinner("Thinking..."):
                answer = qa_responder(st.session_state.summary, user_question)
            st.markdown("---")
            st.markdown("### 🤖 Answer")
            st.markdown(answer)
    
    if st.session_state.transcript:
        lang_code, flag = detect_language(st.session_state.transcript)
        st.markdown(f"### Transcript Language Detected: {flag} ({lang_code})")
        with st.expander("📝 See full transcript"):
            st.text_area("Transcript", format_transcript(st.session_state.transcript), height=300)
        
        st.download_button(
            label="⬇️ Download Summary as .txt",
            data=st.session_state.summary,
            file_name=f"{st.session_state.title}.txt",
            mime="text/plain"
        )
