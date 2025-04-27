import pandas as pd
import os

def load_sentiment_data(filepath):
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        return df
    else:
        raise FileNotFoundError(f"Sentiment results file not found at {filepath}")

# Finbert is said to be tuned towards financial news -> Hence giving it higher preference 
# in cases of conflict

def resolve_sentiment(finbert_sent, vader_sent):
    if finbert_sent == vader_sent:
        return finbert_sent
    elif finbert_sent == "positive" and vader_sent == "neutral":
        return "positive"
    elif finbert_sent == "neutral" and vader_sent == "positive":
        return "positive"
    elif finbert_sent == "negative" and vader_sent == "neutral":
        return "negative"
    elif finbert_sent == "neutral" and vader_sent == "negative":
        return "negative"
    else:
        return "neutral"

def map_sentiment_to_score(sentiment):
    mapping = {
        'positive': 1,
        'neutral': 0,
        'negative': -1
    }
    return mapping.get(sentiment, 0)

def aggregate_industry_sentiments(df):
    df['resolved_sentiment'] = df.apply(
        lambda x: resolve_sentiment(x['finbert_sentiment'], x['vader_sentiment']), axis=1
    )
    df['numeric_sentiment'] = df['resolved_sentiment'].apply(map_sentiment_to_score)

    industry_scores = df.groupby('industry').agg(
        article_count=('resolved_sentiment', 'count'),
        avg_sentiment_score=('numeric_sentiment', 'mean')
    ).reset_index()

    industry_scores = industry_scores.sort_values(by='avg_sentiment_score', ascending=False)
    return df, industry_scores

if __name__ == "__main__":
    input_path = "data/sentiment_results/sentiment_results.csv"
    output_resolved_path = "data/sentiment_results/resolved_sentiments.csv"
    output_sector_scores_path = "data/sentiment_results/sector_sentiment_scores.csv"

    df = load_sentiment_data(input_path)
    df_resolved, industry_scores = aggregate_industry_sentiments(df)

    # Save outputs
    df_resolved.to_csv(output_resolved_path, index=False)
    industry_scores.to_csv(output_sector_scores_path, index=False)

    print("Conflict resolution and industry aggregation complete")
