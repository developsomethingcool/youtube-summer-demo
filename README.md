---
title: YouTube Summarizer
emoji: 📺
colorFrom: indigo
colorTo: blue
sdk: streamlit
sdk_version: "1.32.0"
app_file: app.py
pinned: false
---


# 🎥 YouTube Video Summarizer - HuggingFace Demo Version

A Streamlit-based web application that demonstrates the interface of the YouTube Video Summarizer project.

⚠️ This is a *frontend demo version* deployed on HuggingFace Spaces. The real AI-powered version using Llama3 via Ollama is available locally here: 👉 [Full Dynamic Version on GitHub](https://github.com/developsomethingcool/youtube-summer)

## 📋 Overview

This demo allows you to:
* Paste any YouTube link with captions
* Fetch the video transcript (real API call)
* Display a static example summary
* Provide a static response to any user question
* Download the displayed summary as a text file
* View the detected transcript language

The full AI-powered summarization and Q&A functionality is available only in the local dynamic version.

## 🚀 Try the Live Demo

Available on HuggingFace Spaces: 👉 [Launch Demo](https://huggingface.co/spaces/developsomethingcool/youtube-summarizer-demo)

## 🔧 Installation (Optional for Local Static Version)

1. Clone this repository:
   ```
   git clone https://github.com/developsomethingcool/youtube-summarizer-demo.git
   cd youtube-summarizer-demo
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

## 📚 Project Structure
* `app.py` - Main Streamlit application
* `utils.py` - Helper functions for YouTube transcript retrieval and processing
* `summarizer.py` - Static demo summary text
* `qa.py` - Static demo question-answer response

## ⚙️ Requirements
* Python 3.8+
* Streamlit
* youtube-transcript-api
* pytube
* yt-dlp
* langdetect

No Ollama required in this demo version!

## 🔍 Features
* Real YouTube transcript fetching
* Language detection from transcript
* Clean, interactive Streamlit interface
* Static demo summary
* Static demo Q&A response
* Downloadable summary as text

## ⚠️ Limitations of This Demo
* No real AI summarization or question answering
* Summary & answers are static placeholders
* Full Llama3.1-powered version available only locally

For full functionality: 👉 [Dynamic Ollama-powered Repo](https://github.com/developsomethingcool/youtube-summer)

## 💜 License
This project is MIT licensed.
