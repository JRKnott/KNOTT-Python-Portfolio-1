
---

# Streamlit App Final

## Project Overview

This Streamlit app explores how sentiment compiled from Reddit, and DJIA News (Dow Jones Industrial Average) influences individual stock performance, particularly high-profile stocks like Tesla (TSLA) and Apple (AAPL). The app uses FinBERT—a financial sentiment analysis model—to evaluate Reddit post sentiment and compares it with historical stock trends from Yahoo Finance.


![Screenshot 2025-05-08 222211](https://github.com/user-attachments/assets/a4de4fc0-50c5-4dad-9c63-5e02e73802dd)



The goal is to uncover potential relationships between social media sentiment and market behavior, especially during volatile periods or hype-driven rallies.


---

## Setup & Run Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/JRKnott/StreamlitAppFinal.git
cd StreamlitAppFinal
```

### 2. Setup an Environment

```bash
conda create -n streamlit_env python=3.10
conda activate streamlit_env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually install these libraries:

* `streamlit==1.31.0`
* `pandas==2.2.2`
* `numpy==1.26.4`
* `matplotlib==3.8.4`
* `plotly==5.22.0`
* `praw==7.7.1`
* `psaw==0.0.12`
* `transformers==4.44.2`
* `torch==2.4.1`
* `vaderSentiment==3.3.2`
* `requests==2.32.3`
* `tokenizers==0.19.1`

### 4. Set up Reddit API Credentials

Create a file named `.streamlit/secrets.toml` and add the following:

```toml
[reddit]
client_id = "your_client_id"
client_secret = "your_client_secret"
user_agent = "your_user_agent"
```

### 5. Run App

```bash
streamlit run "FinalProj/pages/Homepage.py"
```

---

# 🧩 App Features

## Homepage

Select on the right-hand side which pages you want to visit.

---

## Effect of Reddit Sentiment on Individual Stocks

**⚠️ Warning:** YFinance may not work if rate limit is reached.
![Screenshot 2025-05-03 183011](https://github.com/user-attachments/assets/50ab2e1b-049d-48a2-9e8f-4ad09a5bb984)
* **Stock Selector:** Choose a stock (e.g., TSLA, AAPL) to analyze.
* **Date Range Picker:** Set custom time windows to compare sentiment and price movement.

**Reddit Sentiment Analysis:**

* Fetches posts from `r/Stocks`, `r/Investing`, or `r/WallStreetBets`. Some may have limited data. Expand date range to find more.
* Analyzes using FinBERT to classify sentiment as Positive, Neutral, or Negative.

**Stock Price Overlay:**

* Visualizes daily closing prices alongside average sentiment scores.

**Downloadable Plots:** Save graphs for offline analysis or presentations.

---

## Sentiment Analysis – VADER (Adjusted to FinBERT) and S\&P 500 Trends

**⚠️ Warning:** May take hours to run. (FinBERT is time-intensive)

*I also have a version that uses VADER. I will attach in a separate document – John.*

**⚠️ Warning:** YFinance may not work if rate limit is reached.

* Uses FinBERT to analyze over 51,000 rows of DJIA news headlines.
* **Adjust Timeframe:** Use the data dropdowns to choose which timeframe you want to analyze.

**First Visualization:** Shows the daily averaged sentiment overlaid with the closing price of the S\&P 500.



*I wanted to make this visualization easier to see, but YF rate limit made troubleshooting impossible. – John*

**Second Visualization:** Shows binned sentiment data in relation to the average next 3 days' closing prices. This shows correlation between sentiment and price movement. *Very interesting!*

* **Select Headline:** A dropdown to select certain headlines and view their sentiment — a fun, interactive feature.

---

## Vader vs. Finbert

![Screenshot 2025-05-08 214529](https://github.com/user-attachments/assets/a0661753-d602-4605-8575-d7cf246dc3ed)


*This was a fun comparison between the two sentiment analyzers. Due to YFinance limits, this is the only part of the code currently confirmed working. Apologies – John*

* **User Input:** Upload a PDF or input text (note: FinBERT has a character limit).

**FinBERT Output:**

* Label: Negative
* Confidence: 0.54

**VADER Output:**

```
Overall VADER Sentiment Scores:
Negative Sentiment: 6.00%
Neutral Sentiment: 84.50%
Positive Sentiment: 9.50%
Overall Sentiment (Compound): 0.7854
Overall Sentiment: Positive
```

![Screenshot 2025-05-08 221553](https://github.com/user-attachments/assets/0b805141-55a5-41a3-bb59-ad3b82681e5b)

* This shows the sentiment of each word in the uploaded text.



**Takeaway:** Although FinBERT is more nuanced, VADER is faster and has unique advantages like flexible compound scores.

---

## References & Resources

* [FinBERT Sentiment Model](https://huggingface.co/ProsusAI/finbert)
* [Streamlit Documentation](https://docs.streamlit.io/)
* [PRAW Reddit API Wrapper](https://praw.readthedocs.io/en/stable/)
* [Yahoo Finance Python Wrapper](https://pypi.org/project/yfinance/)
* [Matplotlib](https://matplotlib.org/)

---

Let me know if you'd like this saved as a `README.md` file or if you need help uploading images to GitHub so they render correctly.











