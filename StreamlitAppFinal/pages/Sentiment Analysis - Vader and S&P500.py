import streamlit as st
st.set_page_config(layout="wide", page_title="Sentiment vs S&P 500")
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import os
from datetime import date
import yfinance as yf
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch
from stqdm import stqdm

# Load FinBERT Sentiment Pipeline
@st.cache_resource
def load_finbert():
    tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
    model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

finbert = load_finbert()

# functions

@st.cache_data
def load_news_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.melt(id_vars=['Date'], value_name='News')
    df = df.dropna(subset=['News'])
    return df

@st.cache_data(show_spinner="Computing FinBERT sentiment...")
def compute_sentiment_finbert(df, batch_size=32):
    sentiments = []
    news_texts = df['News'].astype(str).tolist()
    
    for i in stqdm(range(0, len(news_texts), batch_size), desc="Running FinBERT"):
        batch = news_texts[i:i+batch_size]
        results = finbert(batch)
        
        for r in results:
            if r['label'] == 'positive':
                sentiments.append(r['score'])
            elif r['label'] == 'negative':
                sentiments.append(-r['score'])
            else:  # neutral
                sentiments.append(0.0)
    
    df = df.copy()
    df['sentiment'] = sentiments
    return df

def aggregate_sentiment_by_day(df):
    daily_sentiment = df.groupby('Date').agg(sentiment=('sentiment', 'mean')).reset_index()
    return daily_sentiment

@st.cache_data
def load_sp500_data(start_date, end_date):
    sp500 = yf.download("^GSPC", start=start_date, end=end_date)
    return sp500

# Layout

st.title("Sentiment Analysis of DJIA News and Its Relation to S&P 500 Trends")
st.success("✅ App is running up to here.")

# Load News Data 
try:
    st.write("Loading DJIA news data...")
    news_path = os.path.join(os.getcwd(), 'StreamlitAppFinal', 'pages', 'Combined_News_DJIA.csv')
    if not os.path.exists(news_path):
        st.error(f" File not found: {news_path}")
        st.stop()
    st.write("File path:", news_path)
    
    news_df = load_news_data(news_path)
    st.write(f"✅ News data loaded: {news_df.shape[0]} rows")

    @st.cache_data
    def load_or_compute_sentiment(news_df, cache_path="cached_sentiment.csv"):
        if os.path.exists(cache_path):
            df = pd.read_csv(cache_path, parse_dates=["Date"])
        else:
            df = compute_sentiment_finbert(news_df)
            df.to_csv(cache_path, index=False)
        return df

    news_df = load_or_compute_sentiment(news_df)
    sentiment_df = aggregate_sentiment_by_day(news_df)
except Exception as e:
    st.error(f"❌ Error loading news data: {e}")
    st.stop()

# Sidebar: Date Range Selection 
st.sidebar.title("Date Controls")
start_date = st.sidebar.date_input("Start Date", value=date(2014, 9, 1))
end_date   = st.sidebar.date_input("End Date", value=date(2016, 9, 1))

start_date = pd.to_datetime(start_date)
end_date   = pd.to_datetime(end_date)

# Filter Sentiment Data by Date 
mask = (sentiment_df['Date'] >= start_date) & (sentiment_df['Date'] <= end_date)
filtered_sent = sentiment_df.loc[mask].copy()

# Load and Process S&P 500 Data
try:
    st.write("Loading S&P 500 data...")
    sp500_df = load_sp500_data(start_date, end_date).reset_index()
    st.write(f"✅ S&P 500 data loaded: {sp500_df.shape[0]} rows")
except Exception as e:
    st.error(f"❌ Error loading S&P 500 data: {e}")
    st.stop()

# Calculate Next-Day Returns
sp500_df['return'] = sp500_df['Close'].pct_change()
sp500_df['return_next'] = sp500_df['return'].shift(-1)

returns_map = sp500_df.set_index('Date')['return_next']
filtered_sent['return_next'] = filtered_sent['Date'].map(returns_map)
filtered_sent = filtered_sent.dropna(subset=['return_next'])

# Sentiment vs. S&P 500 Close Plot 
st.subheader("FinBERT Sentiment vs. S&P 500 Close Price")

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(filtered_sent['Date'], filtered_sent['sentiment'], 'b-', label='Sentiment', alpha = .25)
ax1.set_ylabel('FinBERT Sentiment', color='b')
ax1.tick_params(axis='y', labelcolor='b')

ax2 = ax1.twinx()
ax2.plot(sp500_df['Date'], sp500_df['Close'], 'g-', label='S&P 500 Close')
ax2.set_ylabel('S&P 500 Close', color='g')
ax2.tick_params(axis='y', labelcolor='g')

st.pyplot(fig)
plt.close(fig)

# Binned Sentiment vs Return Plot 
st.subheader("Binned Sentiment vs. Next-Day S&P 500 Return")
st.markdown("This shows a binned collection of days by sentiment and shows the range and average of the next day return. In the period of roughly 2013-2016 there was a definite correlation of positive news and price increases, but before 2013 there is no discernible relationship. This may be because of the effects of the 2008 financial crisis and the following recession.")

bins = pd.cut(filtered_sent['sentiment'], np.linspace(-1, 1, 21))
bdf = filtered_sent.copy()
bdf['bin'] = bins

summary = bdf.groupby('bin', observed=False).agg(
    mean_return=('return_next', 'mean'),
    std_return=('return_next', 'std'),
    count=('return_next', 'count')
).reset_index()

summary['center'] = summary['bin'].apply(lambda x: x.mid)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=summary['center'], 
    y=summary['mean_return'],
    mode='lines+markers',
    error_y=dict(type='data', array=summary['std_return']),
    name='Next-Day Return'
))

fig2.update_layout(
    xaxis_title='Sentiment Score',
    yaxis_title='Avg Next-Day Return',
    title='Impact of Sentiment on Next-Day S&P 500 Return'
)
st.plotly_chart(fig2, use_container_width=True)

# News Viewer 
st.subheader("Browse Daily DJIA News Headlines")

if filtered_sent.empty:
    default_date = news_df['Date'].min().date()
else:
    default_date = filtered_sent['Date'].iloc[0].date()

selected_date = st.date_input("Select a Date to View News", value=default_date)
selected_date = pd.to_datetime(selected_date)
daily_news = news_df[news_df['Date'] == selected_date]

if not daily_news.empty:
    for _, row in daily_news.iterrows():
        st.write(f"- {row['News']} (Sentiment: {row['sentiment']:.2f})")
else:
    st.warning("No news available for this date.")