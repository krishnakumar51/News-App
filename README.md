# News Analyzer

![GitHub license](https://img.shields.io/github/license/krishnakumar51/news_summarizer)
![Python version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/Status-Active-green)

Welcome to the **News Analyzer**, a Streamlit-based tool that analyzes recent news articles about a specified company, performs sentiment analysis, and generates audio summaries in both English and Hindi.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)


## Overview
The Company News Analyzer fetches news using the Serp API, analyzes sentiment with the `cardiffnlp/twitter-roberta-base-sentiment` model, and generates dual-language audio summaries using `gTTS`.

## Features
- **News Fetching**: Retrieves up to 10 recent news articles per company.
- **Sentiment Analysis**: Classifies articles as Positive, Negative, or Neutral.
- **Dual-Language Summaries**: Generates text and audio in English and Hindi.
- **User-Friendly Interface**: Streamlit UI with audio playback.

## Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/krishnakumar51/Company-News-Analyser.git
   cd Company-News-Analyser
2. **Create a Virtual Environment**
   ```bash
    python -m venv venv
    source venv/bin/activate  
3. **Install Dependencies Install the required Python packages:**
    ```bash
    pip install -r requirements.txt
4. **Set Up Environment Variables**
    Create a local .env file (do not commit this to Git)
    ```bash 
    SERP_API_KEY=<API-key>
    GROQ_API_KEY=<API-key>
5. **Run the Application**
    ```bash
    streamlit run app.py

## Usage

- Open your browser and navigate to http://localhost:8501 (Streamlit default port).
- Enter a company name (e.g., "nvidia" or "tesla") in the text input field.
- Click the "Analyze" button to fetch articles, analyze sentiment, and generate summaries.
- View the articles, sentiment breakdown, and listen to the English and Hindi audio summaries.
