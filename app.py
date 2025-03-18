import streamlit as st
from utils import fetch_news_report, generate_comparative_analysis, generate_audio_files

st.set_page_config(page_title="Company News Analyzer", layout="wide")
st.title("Company News Analyzer")
st.header("Enter Company Details")
company = st.text_input("Enter company name")

if st.button("Analyze"):
    with st.spinner("Analyzing company news..."):
        articles = fetch_news_report(company)
        analysis = generate_comparative_analysis(articles, company)
        audio_urls = generate_audio_files(company, analysis)

    if articles:
        st.subheader(f"News Articles for {company}")
        for article in articles:
            st.write(f"**Title:** {article['Title']}")
            st.write(f"**Summary:** {article['Summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
            st.write("---")
        
        st.subheader("Sentiment Analysis Summary")
        sentiment_dist = analysis["Sentiment Distribution"]
        st.write(f"**Positive:** {sentiment_dist['Positive']}")
        st.write(f"**Negative:** {sentiment_dist['Negative']}")
        st.write(f"**Neutral:** {sentiment_dist['Neutral']}")
        
        st.subheader("Final Verdict")
        st.write(f"**English Summary:** {analysis['Summary']}")
        st.write(f"**Hindi Summary:** {analysis['Hindi Summary']}")
        st.audio(audio_urls["English"])
        st.audio(audio_urls["Hindi"])
    else:
        st.error("No articles found or error occurred.")