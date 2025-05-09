import streamlit as st
import matplotlib.pyplot as plt
import PyPDF2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Set page config
st.set_page_config(page_title="Sentiment Analysis App", layout="wide")
st.title("Comparing Sentiment Analyzers")
st.markdown("### Vader vs Finbert")
st.markdown("""
Upload a PDF or type/paste text below to analyze sentiment using either **FinBERT** or **VADER**.
Use this page to compare the differences in these two popular Sentiment Analyzers.
""")

# Load FinBERT pipeline
@st.cache_resource
def load_finbert_pipeline():
    model = AutoModelForSequenceClassification.from_pretrained("yiyanghkust/finbert-tone")
    tokenizer = AutoTokenizer.from_pretrained("yiyanghkust/finbert-tone")
    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Load VADER
@st.cache_resource
def load_vader():
    return SentimentIntensityAnalyzer()

finbert = load_finbert_pipeline()
vader = load_vader()


# PDF or Text Input
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
text_input = st.text_area("Or paste/type your text here:", value = """Nvidia CEO Jensen Huang said in an interview on Tuesday that it would be a "tremendous loss" to be blocked from China's AI market.
The Trump administration restricted the shipment of Nvidia's H20 chips to China without a license last month, leading to a $5.5 billion quarterly charge.
"Let us get the American AI out in front of everybody right now," Huang said at ServiceNow's Knowledge 2025 conference in Las Vegas.
Nvidia CEO Jensen Huang said on Tuesday that China's artificial intelligence market will likely reach about $50 billion in the next two to three years, and that missing out on it would be a "tremendous loss."

Huang said being able to sell into China would bring back revenue, taxes, and "create lots of jobs here in the United States."

"We just have to stay agile," Huang told CNBC's Jon Fortt, in an interview alongside ServiceNow CEO Bill McDermott. The tech execs were in Las Vegas for ServiceNow's Knowledge 2025 conference. "Whatever the policies are of the government, whatever is in the best interest of our country, we'll support," Huang said."""
 )

# Extract text from PDF if uploaded
def extract_pdf_text(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

if uploaded_file is not None:
    text = extract_pdf_text(uploaded_file)
elif text_input.strip():
    text = text_input.strip()
else:
    text = ""

if text:
    st.subheader("Sentiment Analysis Result")

    # Create columns for side-by-side comparison
    col1, col2 = st.columns(2)
    
    # FinBERT result
    with col1:
        st.markdown("### Finbert Sentiment Analysis")
        results = finbert(text)
        for res in results:
            st.markdown(f"**Label**: {res['label']}")
            st.markdown(f"**Confidence**: {res['score']:.2f}")

        # Plot FinBERT probabilities
        labels = [res['label'] for res in results]
        scores = [res['score'] for res in results]
        fig, ax = plt.subplots()
        ax.bar(labels, scores, color=['green' if l == 'positive' else 'red' if l == 'negative' else 'gray' for l in labels])
        ax.set_ylabel("Probability")
        ax.set_title("Finbert Sentiment Scores")
        st.pyplot(fig)

    # VADER result
    with col2:
        st.markdown("### VADER Sentiment Analysis")
        scores = vader.polarity_scores(text)
        st.markdown("**Overall VADER Sentiment Scores**:")
        
        # Cleaner formatting of VADER output
        st.markdown(f"**Negative Sentiment**: {scores['neg']*100:.2f}%")
        st.markdown(f"**Neutral Sentiment**: {scores['neu']*100:.2f}%")
        st.markdown(f"**Positive Sentiment**: {scores['pos']*100:.2f}%")
        st.markdown(f"**Overall Sentiment (Compound)**: {scores['compound']:.4f}")

        # Display a message based on the compound score
        if scores['compound'] >= 0.05:
            sentiment_label = "Positive"
        elif scores['compound'] <= -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        st.markdown(f"**Overall Sentiment**: {sentiment_label}")

        # Token-level sentiment analysis
        st.markdown("#### Token-Level Vader Sentiment")
        st.markdown("This can help you see what words VADER is taking into account when deriving sentiment from text.")
        words = text.split()
        colored_text = []

        # Loop over each word and analyze sentiment
        for word in words:
            val = vader.polarity_scores(word)['compound']
            if val >= 0.3:
                colored_text.append(f"🟢 {word} (Positive)")
            elif val <= -0.3:
                colored_text.append(f"🔴 {word} (Negative)")
            else:
                colored_text.append(f"⚪ {word} (Neutral)")

        # Display the token-level sentiment
        st.markdown(" ".join(colored_text))