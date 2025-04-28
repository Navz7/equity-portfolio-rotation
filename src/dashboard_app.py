import streamlit as st
import pandas as pd

# Set Streamlit page config
st.set_page_config(page_title="Equity Portfolio Rotation", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sentiment_results/sector_sentiment_scores.csv")
    return df

df = load_data()

st.title("🏦 Equity Portfolio Rotation Dashboard")

st.subheader("🏆 Top Performing Sectors by Sentiment")
st.dataframe(df.head(5))

st.subheader("📉 Bottom Performing Sectors by Sentiment")
st.dataframe(df.tail(5))

st.subheader("📊 Sector Sentiment Scores")
st.bar_chart(df.set_index('industry')['avg_sentiment_score'])
