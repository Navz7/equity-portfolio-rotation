import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set Streamlit page config
st.set_page_config(page_title="Equity Portfolio Rotation", layout="wide")

# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("data/sentiment_results/sector_sentiment_scores.csv")
    return df

df = load_data()

st.title("⚖️ Equity Portfolio Rotation Dashboard")

st.subheader("🏆 Top Performing Sectors by Sentiment")
st.dataframe(df.head(5))

st.subheader("📉 Bottom Performing Sectors by Sentiment")
st.dataframe(df.tail(5))

st.subheader("📊 Sector Sentiment Scores")
st.bar_chart(df.set_index('industry')['avg_sentiment_score'])

df['score_adj'] = df['avg_sentiment_score'].clip(lower=0)
df['weight'] = df['score_adj'] / df['score_adj'].sum()
df['percentage'] = df['weight'] * 100
df = df[df['percentage']!=0]


st.subheader("📈 Recommended Portfolio Allocation by Sector")

fig, ax = plt.subplots(figsize=(4, 4)) 
ax.pie(df['percentage'], labels=df['industry'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')
plt.tight_layout()
st.pyplot(fig, bbox_inches='tight', use_container_width=False)