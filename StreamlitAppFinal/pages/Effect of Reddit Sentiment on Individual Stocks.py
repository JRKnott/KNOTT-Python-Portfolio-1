import streamlit as st
import praw
from transformers import pipeline
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
import logging
import torch
import hashlib
import json

# Device setup
device = torch.device("cpu")  # Use CPU

# Streamlit Cache Helper for Sentiment Input Hashing 
def hash_post_titles(posts):
    key = [(p.title, p.created_utc) for p in posts]
    return hashlib.md5(json.dumps(key).encode()).hexdigest()

# Cache FinBERT Pipeline (Loaded Once) --
@st.cache_resource
def load_finbert_pipeline():
    return pipeline("sentiment-analysis", model="ProsusAI/finbert", top_k=None, device=-1)


sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", top_k=None, framework="pt", device=-1)

#Keyword Mapping 
ticker_mapping = {
    'AAPL': ['aapl', 'apple', 'iphone', 'macbook'],
    'MSFT': ['msft', 'microsoft', 'windows', 'xbox'],
    'AMZN': ['amzn', 'amazon', 'aws', 'prime'],
    'GOOGL': ['googl', 'google', 'alphabet', 'android'],
    'TSLA': ['tsla', 'tesla', 'elon', 'cybertruck'],
    'NVDA': ['nvda', 'nvidia', 'jensen', 'huang', 'blackwell'],
    'META': ['meta', 'facebook', 'instagram', 'whatsapp', 'oculus'],
    'AMD': ['amd', 'ryzen', 'radeon', 'epyc'],
    'INTC': ['intc', 'intel', 'core i9', 'xeon']
}


# Cache Reddit Posts 
@st.cache_data
def get_reddit_posts(ticker, subreddit, days_back=30, max_posts=100):
    reddit = praw.Reddit(
            client_id= CLIENT_ID,
            client_secret= CLIENT_SECRET,
            user_agent= USER_AGENT
    )

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days_back)
    posts = []

    try:
        submissions = reddit.subreddit(subreddit).top(time_filter='all', limit=None)
        for submission in submissions:
            submission_time = datetime.utcfromtimestamp(submission.created_utc)
            if start_time <= submission_time <= end_time:
                text = (submission.title + " " + (submission.selftext or "")).lower()
                if any(keyword in text for keyword in ticker_mapping[ticker]):
                    posts.append(submission)
                    if len(posts) >= max_posts:
                        break
    except Exception as e:
        logging.error("Error fetching Reddit posts", exc_info=True)
        return []

    return posts

# Cache Sentiment Analysis Results
@st.cache_data(show_spinner=False)
def analyze_sentiment(texts):
    results = sentiment_pipeline(texts, truncation=True, max_length=512)
    labels = []
    scores = []
    for res in results:
        top = max(res, key=lambda x: x['score'])
        labels.append(top['label'].lower())
        scores.append(top['score'])
    return labels, scores

# Cache Stock Data
@st.cache_data
def fetch_stock_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise ValueError(f"No data found for {ticker}")
        return data
    except Exception as e:
        logging.error(f"Stock data fetch failed: {e}")
        return pd.DataFrame()
    
# Streamlit App UI
st.title("Stock Sentiment Analysis of Notable Reddit Posts with FinBERT")
st.info("Fetching notable Reddit posts may take 5–20 seconds the first time, then loads faster via caching.")

tickers = list(ticker_mapping.keys())
selected_ticker = st.selectbox("Select a stock ticker", tickers)

subreddits = ['stocks', 'investing', 'wallstreetbets']
selected_subreddit = st.selectbox("Select a subreddit", subreddits)

periods = [30, 90, 180, 365, 730, 1095, 3650]
selected_period = st.selectbox("Select time period (days)", periods, index=0)

# get Reddit Posts
with st.spinner("Fetching Reddit posts..."):
    posts = get_reddit_posts(selected_ticker, selected_subreddit, selected_period, max_posts=200)

post_data = []
for post in posts:
    date = datetime.fromtimestamp(post.created_utc).date()
    text = post.title + " " + (post.selftext or "")
    post_data.append({'date': date, 'text': text})
df_posts = pd.DataFrame(post_data)

# Analyze Sentiment
if not df_posts.empty:
    with st.spinner("Analyzing sentiment with FinBERT..."):
        texts = df_posts['text'].tolist()
        labels, scores = analyze_sentiment(texts)
        df_posts['sentiment_label'] = labels
        df_posts['sentiment_score'] = scores

        label_counts = df_posts['sentiment_label'].value_counts()
        st.write("Sentiment Label Distribution:", label_counts)

        df_sentiment_by_day = df_posts.groupby(['date', 'sentiment_label']).size().unstack(fill_value=0)
        df_sentiment_prop = df_sentiment_by_day.div(df_sentiment_by_day.sum(axis=1), axis=0)
        df_sentiment_prop.index = pd.to_datetime(df_sentiment_prop.index)
else:
    df_sentiment_prop = pd.DataFrame()
    st.warning(f"No notable posts found for {selected_ticker} in r/{selected_subreddit}.")

# Fetch Stock Data
with st.spinner("Fetching stock price data..."):
    start_date = datetime.now() - timedelta(days=selected_period)
    end_date = datetime.now()
    stock_data = fetch_stock_data(selected_ticker, start=start_date, end=end_date)

# Plot Results
if not stock_data.empty:
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(10, 6))

    # 1. stock price
    ax1.plot(stock_data.index, stock_data['Close'], label='Stock Price', color='blue')
    ax1.set_title(f"{selected_ticker} Stock Price")
    ax1.set_ylabel("Price ($)")
    ax1.grid(True)

    # 2. sentiment plot
    if not df_sentiment_prop.empty:
        aligned = df_sentiment_prop.reindex(stock_data.index, method='nearest', tolerance=pd.Timedelta(days=1)).ffill()
        for sentiment in ['positive', 'neutral', 'negative']:
            if sentiment in aligned.columns:
                ax2.plot(aligned.index, aligned[sentiment], label=sentiment.capitalize())
        ax2.set_title("Reddit Sentiment Proportions")
        ax2.set_ylabel("Proportion")
        ax2.legend()
        ax2.grid(True)
    else:
        ax2.set_title("No Sentiment Data")
        ax2.set_ylabel("Sentiment Score")
        ax2.grid(True)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
else:
    st.warning("No stock data available...")
