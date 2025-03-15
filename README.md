# Financial News Ranking System

This project is a **Financial News Ranking System** designed to analyze and rank news articles based on their potential impact on financial markets. It uses advanced natural language processing (NLP) techniques to evaluate sentiment, financial relevance, and market-moving potential.

## Features

- **Sentiment Analysis**: Predicts the sentiment (positive, negative, neutral) of news articles.
- **Financial Relevance**: Identifies key financial entities and market-moving verbs.
- **Source Credibility**: Scores news sources based on their historical credibility.
- **Market Impact Ranking**: Combines multiple metrics to rank articles by their potential market impact.

## How It Works

1. **Fetch Raw News**: The system fetches raw news articles from a news API.
2. **Process Data**: Articles are processed to extract key fields like title, content, description, and source.
3. **Sentiment Analysis**: Sentiment labels and scores are predicted using a pre-trained NLP model.
4. **Rank Articles**: Articles are ranked based on their market impact score, which combines sentiment strength, financial relevance, novelty, and source credibility.

## Technologies Used

- **Python**: Core programming language.
- **FastAPI**: For building the REST API.
- **Pandas**: For data manipulation and analysis.
- **TextBlob**: For sentiment analysis.
- **Hugging-Face Pipeline**: FinBert model For sentiment Prediction.


## Features

- **Sentiment Analysis**: Predicts the sentiment (positive, negative, neutral) of news articles using the `ProsusAI/finbert` model.
- **Financial Relevance**: Identifies key financial entities and market-moving verbs.
- **Source Credibility**: Scores news sources based on their historical credibility.
- **Market Impact Ranking**: Combines multiple metrics to rank articles by their potential market impact.
- **Customizable Ranking**: Supports multiple ranking strategies (e.g., `market_importance`, `sentiment`).

## Ranking Types

The system supports multiple ranking strategies. You can specify the ranking type using the `ranking_type` query parameter in the `/api/v1/ranking/news` endpoint.

### Available Ranking Types

1. **`market_importance` (Default)**:
   - Combines multiple factors to rank articles by their potential market impact.
   - Metrics:
     - **Sentiment Strength**: Measures the intensity of sentiment (positive/negative).
     - **Entity Density**: Counts mentions of financial entities (e.g., "stocks", "bonds").
     - **Market Verbs**: Counts action verbs that typically move markets (e.g., "acquire", "merge").
     - **Novelty Score**: Measures the uniqueness of the article content.
     - **Source Credibility**: Scores the credibility of the news source.
   - Formula:
     ```
     market_impact = (sentiment_strength * 0.3) + (entity_density * 0.25) +
                     (market_verbs * 0.2) + (novelty_score * 0.15) + (source_credibility * 0.1)
     ```

2. **`sentiment`**:
   - Ranks articles based on their sentiment score and label.
   - Positive articles with high sentiment scores rank highest.
   - Negative articles with high sentiment scores rank lowest.
   - Formula:
     ```
     sentiment_rank = sentiment_score * sentiment_label_weight
     ```
     - `sentiment_label_weight`:
       - `POSITIVE`: 1.0
       - `NEGATIVE`: -1.0
       - `NEUTRAL`: 0.0



## Configuration (`config.yaml`)

The system is configured using a `config.yaml` file. 



2. ## Requirement

- python 3.8 or later


#### Install python using Miniconda

1) Download and install from [here]:  
```bash 
git clone https://github.com/your-username/financial-news-ranking-system.git
```
2) Create a new environment usind this command: 
```bash 
$ conda create -n venv python=3.8 
```

3) Activit the environment: 
```bash
$ conda activate venv
```

```bash
$ pip install -r requirement.txt
```

setup the environment variables:

```bash
$ cp .env.example .env 
```

set your environment variables in the `.env` file like your `NEWS_API_KEY` value.


## run the FAST API server

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 8000
```