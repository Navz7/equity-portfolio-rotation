import json
import os
import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
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
                "sentiment": result[0]['label'],
                "confidence": result[0]['score']
            })
        except Exception as e:
            return pd.Series({"sentiment": "ERROR", "confidence": 0.0})

    # Apply sentiment to DataFrame
    sentiment_df = df[text_col].progress_apply(get_sentiment)
    return pd.concat([df, sentiment_df], axis=1)


# Load model just once
finbert_model_name = "ProsusAI/finbert"
tokenizer = BertTokenizer.from_pretrained(finbert_model_name)
model = BertForSequenceClassification.from_pretrained(finbert_model_name)
finbert = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

raw_data_dir = 'data/raw_news'
all_articles = load_raw_data(raw_data_dir)

df = preprocess_articles(all_articles)

#Applying Sentiment analysis to existing df--> sentiment + confidence will be tracked.
df = apply_finbert_sentiment(df, text_col='text')
print(df.head())