# NLP Driven Equity Portfolio Dashboard - By Navneeth Anil Kumar

# 📈📉Equity Portfolio Rotation Reccomendation Engine

This project is a sentiment analysis dashboard that helps recommend equity sector allocations based on the tone of financial news headlines. By leveraging powerful NLP models (FinBERT and VADER) and visualized through Streamlit. The dashboard suggests which sectors show the most optimism in the market — allowing for smarter portfolio rotation decisions. 

---

## 📋 Methodology

-  Ingests financial news headlines by sector using **NewsAPI**
-  Applies **FinBERT** (BERT trained specifically on financial data) and **VADER** for sentiment scoring
-  Resolves conflicting sentiment using custom logic (Higher preference given for FinBERT)
-  Aggregates sentiment by **industry/sector**
-  Generates a pie chart with **recommended portfolio weights**
-  Visualizes top/bottom performing sectors, KPIs, and sentiment scores

---

## 🧠 Technologies Used

- `Python` — core logic
- `pandas` — data cleaning and aggregation
- `Streamlit` — for building the interactive dashboard
- `transformers` + `FinBERT` — financial sentiment analysis
- `VADER` — rule-based sentiment scoring
- `matplotlib` — pie and bar charts
- `NewsAPI` — for fetching relevant news that'll drive our recommendation

---

## ⚠️Risks and Potential Improvements

- NewsAPI only returns limited reports. We should assign a minimum threshold for number of reports per industry from trusted sources to build a robust solution.
- NewsAPI can be replaced with **Google News** as the search queries are much more efficient.
- Couple the existing project with real world financial data to back the decisions. 
- Build an app where the user can input their existing equity industry allocation, and the app provides recommendations on which sectors to rotate their money to.

---