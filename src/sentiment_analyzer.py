import json
import os
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
from tqdm import tqdm


def load_raw_data(raw_data_dir):
    all_articles = []

    # Iterate through each file in the raw data directory
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Get the industry tag from the filename (e.g., "banking_20250420.json" -> "banking")
                    industry = filename.split('_')[0]

                    # If data is a list and non-empty, tag each with industry and add to all_articles
                    if isinstance(data, list) and data:
                        for article in data:
                            article['industry'] = industry
                            all_articles.append(article)
                    else:
                        print(f"No articles found or empty content in {filename}.")
            
            except json.JSONDecodeError:
                print(f"Error decoding JSON in {filename}. Skipping this file.")
            except Exception as e:
                print(f"An error occurred with file {filename}: {e}")

    return all_articles

def preprocess_articles(articles):
    processed_data = []
    
    for article in articles:
        title = article.get('title', '')
        description = article.get('description', '')
        published_at = article.get('publishedAt', '')
        source = article['source'].get('name', '') if article.get('source') else ''
        industry = article.get('industry', '')

        # Add more preprocessing like cleaning text (lowercase, removing special characters, etc.)
        # For now, we're just collecting the basic info
        processed_data.append({
            'title': title,
            'description': description,
            'published_at': published_at,
            'source': source,
            'industry': industry
        })
    
    df = pd.DataFrame(processed_data)
    df['text'] = df['title'].fillna('') + '. ' + df['description'].fillna('')
    return df

def apply_finbert_sentiment(df, text_col='text'):
    tqdm.pandas()  # Enables progress bar
    
    def get_sentiment(text):
        try:
            result = finbert(text[:512])  # BERT limit
            return pd.Series({
                "finbert_sentiment": result[0]['label'],
                "finbert_score": result[0]['score']
            })
        except Exception as e:
            return pd.Series({"finbert_sentiment": "ERROR", "finbert_score": 0.0})

    # Apply sentiment to DataFrame
    sentiment_df = df[text_col].progress_apply(get_sentiment)
    return pd.concat([df, sentiment_df], axis=1)

def apply_vader_sentiment(df, text_col='text'):
    tqdm.pandas()
    analyzer = SentimentIntensityAnalyzer()

    def get_vader_sentiment(text):
        try:
            score = analyzer.polarity_scores(text)['compound']
            if score >= 0.05:
                sentiment = 'positive'
            elif score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            return pd.Series({
                "vader_sentiment": sentiment,
                "vader_score": score
            })
        except Exception as e:
            return pd.Series({
                "vader_sentiment": "ERROR",
                "vader_score": 0.0
            })

    vader_df = df[text_col].progress_apply(get_vader_sentiment)
    return pd.concat([df, vader_df], axis=1)

# Load model just once
finbert_model_name = "ProsusAI/finbert"
tokenizer = BertTokenizer.from_pretrained(finbert_model_name)
model = BertForSequenceClassification.from_pretrained(finbert_model_name)
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

raw_data_dir = 'data/raw_news'
all_articles = load_raw_data(raw_data_dir)

df = preprocess_articles(all_articles)

#Applying finbert Sentiment analysis to existing df--> sentiment + confidence will be tracked.
df = apply_finbert_sentiment(df, text_col='text')
# Incorporating vader sentiment analysis as a secondary check -> There may be chances of conflicting info from diff news sources.
df = apply_vader_sentiment(df, text_col='text')
out_path = "/mnt/c/Users/LENOVO/Documents/EquityPortfolioRotation/equity-portfolio-rotation/data/sentiment_results/sentiment_results.csv"
df.to_csv(out_path, index=False)