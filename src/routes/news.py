from fastapi import APIRouter, Query, Depends, HTTPException
import requests
from src.controllers.news_controller import NewsController
from src.enums.messages_enum import Messages
from config.app_config import load_config
from src.helpers.log_helper import Logger  # Import logger helper

news_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])

# Initialize logger
log_instance = Logger(log_name="api_requests_news")
logger = log_instance.get_logger()


def get_news_controller():
    """
    Dependency injection function to provide a single instance of NewsController.

    Returns:
        NewsController: An instance of the NewsController class.
    """
    return NewsController()


@news_router.get("/fetch-raw-news")
async def fetch_raw_news(
    query: str = Query(
        ...,
        description=f"Search for finance-related news ({', '.join(load_config().news.allowed_queries)})",
    ),
    news_controller: NewsController = Depends(get_news_controller),
):
    """
    Fetches raw finance-related news articles based on the given query and saves them to a file.

    Args:
        query (str): The finance-related search term (e.g., "stock market").
        news_controller (NewsController): The dependency-injected instance of NewsController.

    Returns:
        dict: JSON response containing raw news articles.
    """
    logger.info(f"Received API request with query='{query}'")

    try:
        # Generate API URL
        formatted_url = news_controller.process_api_link(query)
        logger.info(f"Fetching news from API: {formatted_url}")
        response = requests.get(formatted_url)

        if response.status_code != 200:
            logger.error(f"Failed to fetch news: {response.json()}")
            return {"message": Messages.FETCH_FAILURE.value, "data": []}

        # Get raw articles
        raw_articles = response.json().get("articles", [])
        logger.info(f"Fetched {len(raw_articles)} articles successfully.")

        # Save raw articles to a file
        save_status = news_controller.save_raw_data(raw_articles)

        return {
            "message": Messages.FETCH_SUCCESS.value,
            "save_status": save_status,
            "data": raw_articles,
        }

    except ValueError as e:
        logger.error(f"Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))

    except requests.exceptions.RequestException as e:
        logger.error(f"API Request Error: {e}")
        return {"message": Messages.FETCH_FAILURE.value, "data": []}

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"message": "An unexpected error occurred.", "data": []}


@news_router.get("/apply-sentiment")
async def apply_sentiment(
    news_controller: NewsController = Depends(get_news_controller),
):
    """
    Reads raw news articles from a file, performs sentiment analysis, and saves the results to another file.

    Args:
        news_controller (NewsController): The dependency-injected instance of NewsController.

    Returns:
        dict: JSON response containing processed and sentiment-predicted news articles.
    """
    logger.info("Received request to analyze sentiment on raw news data.")

    try:
        # Read raw articles from the file
        raw_articles = news_controller.read_raw_data()
        if not raw_articles:
            logger.warning("No raw articles found to process.")
            return {"message": Messages.PROCESS_FAILURE.value, "data": []}

        # Process the articles
        processed_articles = news_controller.processing_data(raw_articles)
        if not processed_articles:
            logger.warning("No valid articles found after processing.")
            return {"message": Messages.PROCESS_FAILURE.value, "data": []}

        # Apply sentiment prediction to the articles
        try:
            processed_articles = news_controller.predict_model(processed_articles)
            logger.info("Sentiment prediction completed successfully.")
        except Exception as pred_e:
            logger.error(f"Error during sentiment prediction: {pred_e}")
            return {"message": Messages.MODEL_PREDICTION_FAILURE.value, "data": []}

        # Save processed articles to CSV
        save_status = news_controller.save_processing_data(processed_articles)

        return {
            "message": Messages.PROCESS_SUCCESS.value,
            "save_status": save_status,
            "data": processed_articles,
        }

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {"message": "An unexpected error occurred.", "data": []}
