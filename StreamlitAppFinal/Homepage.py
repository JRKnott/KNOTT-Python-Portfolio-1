import streamlit as st

# Set up the title of the home page
st.title("Financial Insights through Sentiment Analysis")

# Provide a brief explanation of what the app does
st.markdown("""
### Project Overview

This project utilizes sentiment analysis to analyze the relationship between retail sentiment
and stock market data, specifically the daily closing price of the S&P 500 and individual stocks such as Tesla (TSLA). 
I used models such as FinBERT to extract sentiments from financial data and apply 
this information to help identify market trends.

            """)

st.image("https://nairametrics.com/wp-content/uploads/2023/06/green-bull-market-run-upward-presents-uptrend-stock-market-financial-business-concept-generative-ai_1423-7210.jpeg", use_column_width=True)

st.markdown("""
### Features of the App:
- Sentiment analysis on Reddit posts (WallStreetBets)
- Comparison of sentiment trends with stock data (e.g., Tesla, S&P 500)
- Interactive visualizations of stock trends and sentiment analysis
- Ability to filter and analyze different time frames
- Comparison of different sentiment analyzers

### How to Use:
1. Use the navigation on the sidebar to access different pages:
   - **Effect of Reddit Sentiment on Individual Stocks**: See the relationship between market sentiment and individual stocks.
   - **Sentiment Analysis - Vader and S&P500**: Compare basic sentiment with overall market trends .
   - **Vader vs. Finbert**: Compare two popular sentiment analyzers.
   
2. Select the data and timeframes you are interested in to explore the insights.
   
Please leave any feedback on my Github: https://github.com/JRKnott 
            
""")


