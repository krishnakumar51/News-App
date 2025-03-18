import os
import re
from gtts import gTTS
from deep_translator import GoogleTranslator
from transformers import pipeline
from langchain_groq import ChatGroq
from serpapi import GoogleSearch
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, groq_api_key=GROQ_API_KEY)
sentiment_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment")

def fetch_news_report(company: str) -> list:
    """Fetch news articles using Serp API."""
    articles = []
    try:
        params = {
            "engine": "google",
            "q": f"recent news articles about {company}",
            "tbm": "nws",
            "num": 10,
            "api_key": SERP_API_KEY
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results.get("news_results", [])
        for article in news_results[:10]:
            title = article.get("title")
            summary = article.get("snippet")
            if title and summary:
                sentiment = analyze_sentiment(summary)
                articles.append({
                    "Title": title,
                    "Summary": summary,
                    "Sentiment": sentiment,
                    "Topics": extract_topics(summary)
                })
    except Exception as e:
        print(f"[ERROR] Error fetching news: {str(e)}")
    return articles

def analyze_sentiment(text: str) -> str:
    """Analyze sentiment of the text."""
    result = sentiment_pipeline(text[:512])[0]
    label = result["label"]
    if label == "LABEL_0":
        return "Negative"
    elif label == "LABEL_1":
        return "Neutral"
    elif label == "LABEL_2":
        return "Positive"
    return "Unknown"

def extract_topics(text: str) -> list:
    """Extract key topics using the language model."""
    prompt = f"Extract 3 key topics from this text: {text}"
    response = llm.invoke(prompt)
    topics = response.content.split("\n")[:3]
    return [topic.strip() for topic in topics if topic.strip()]

def generate_comparative_analysis(articles: list, company: str) -> dict:
    """Generate sentiment distribution and summaries across articles."""
    sentiment_dist = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment = article.get("Sentiment", "Neutral")
        sentiment_dist[sentiment] += 1
    
    total = len(articles)
    english_summary = (f"Out of {total} articles about {company if articles else 'the company'}, "
                      f"{sentiment_dist['Positive']} were positive, "
                      f"{sentiment_dist['Negative']} were negative, "
                      f"and {sentiment_dist['Neutral']} were neutral.")
    
    translator = GoogleTranslator(source='en', target='hi')
    hindi_summary = translator.translate(english_summary)
    
    return {
        "Sentiment Distribution": sentiment_dist,
        "Summary": english_summary,
        "Hindi Summary": hindi_summary
    }

def generate_audio_files(company: str, analysis: dict) -> dict:
    """Generate English and Hindi audio files and return their URLs."""
    safe_company = re.sub(r'\W+', '_', company.lower())
    os.makedirs("static", exist_ok=True)
    
    english_audio_path = os.path.join("static", f"{safe_company}_summary_en.mp3")
    tts_en = gTTS(text=analysis["Summary"], lang="en")
    tts_en.save(english_audio_path)
    
    hindi_audio_path = os.path.join("static", f"{safe_company}_summary_hi.mp3")
    tts_hi = gTTS(text=analysis["Hindi Summary"], lang="hi")
    tts_hi.save(hindi_audio_path)
    
    base_url = "https://" + os.getenv("HF_SPACE_NAME", "localhost:7860")
    audio_urls = {
        "English": f"{base_url}/static/{safe_company}_summary_en.mp3",
        "Hindi": f"{base_url}/static/{safe_company}_summary_hi.mp3"
    }
    return audio_urls