from src.controllers.base_controller import BaseController
import pandas as pd

from src.enums.messages_enum import Messages
from src.models.sentiment_model import SentimentModelHandler


class NewsController(BaseController):
    """
    Controller for processing news-related API requests.
    """

    def __init__(self):
        """
        Initializes the NewsController by inheriting from BaseController.
        """
        super().__init__()

    def process_api_link(self, query: str) -> str:
        """
        Processes and formats the News API link based on the provided query.

        Args:
            query (str): The finance-related search query (e.g., "stock market").

        Returns:
            str: The formatted API URL ready for the request.

        Raises:
            ValueError: If the query is not in the allowed list.
        """
        # Validate query against allowed queries in config.yaml
        if query.lower() not in [
            q.lower() for q in self.app_config.news.allowed_queries
        ]:
            raise ValueError(
                f"Invalid query: '{query}'. Allowed queries are: {self.app_config.news.allowed_queries}"
            )

        # Generate API URL for query-based search
        return self.app_config.news.query_url.format(
            query=query,
            api_key=self.env_config.NEWS_API_KEY,
        )

    def processing_data(self, news: list) -> list[dict]:
        """
        Processes a list of news articles by extracting and combining content and descriptions.

        Args:
            news (list): A list of dictionaries containing news articles.

        Returns:
            list[dict]: A list of processed articles with title, content, description, and combined text.
        """
        if not news:
            return []  # Return empty list if no data

        processed_articles = []
        for article in news:
            try:
                content = article.get("content", "").strip()
                description = article.get("description", "").strip()
                title = article.get("title", "No Title").strip()

                # Skip articles with no title or empty content/description
                if not title or (not content and not description):
                    continue

                # Combine content & description for ranking
                full_text = f"{description} {content}".strip()

                # Store processed data
                processed_articles.append(
                    {
                        "title": title,
                        "content": content,
                        "description": description,
                        "text": full_text,
                    }
                )
            except Exception:
                continue  # Skip invalid articles to prevent crashing

        return processed_articles

    def save_processing_data(
        self,
        processed_articles: list[dict],
        file_path: str = "assets\processed_news.csv",
    ):
        """
        Saves the processed news articles into a CSV file.

        Args:
            processed_articles (list[dict]): A list of processed news articles.
            file_path (str, optional): The file path to save the CSV file. Defaults to "processed_news.csv".

        Returns:
            None
        """
        if not processed_articles:
            return Messages.PROCESS_FAILURE.value

        try:
            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(processed_articles)

            # Save DataFrame to CSV
            df.to_csv(file_path, index=False, encoding="utf-8")
        except Exception:
            pass  # Silently fail if there's an issue writing the file
        return Messages.PROCESS_SUCCESS.value

    def predict_model(self, articles: list[dict]) -> list[dict]:
        """
        Applies sentiment analysis to each article and adds the prediction results.

        Args:
            articles (list[dict]): A list of processed news articles.

        Returns:
            list[dict]: The list of articles updated with sentiment labels and scores.
        """
        if not articles:
            return articles

        try:
            # Instantiate and load the sentiment model
            sentiment_model = SentimentModelHandler(
                model_name=self.app_config.models.sentiment_analysis_model.name,
            )
            sentiment_model.load_model()

            # Apply sentiment prediction for each article based on the combined text field
            for article in articles:
                text = article.get("text", "")
                prediction = sentiment_model.predict(text)
                article["sentiment_label"] = prediction.get("label", "NEUTRAL")
                article["sentiment_score"] = prediction.get("score", 0.0)
        except Exception as e:
            # self.logger.error(f"Error during sentiment prediction: {e}")
            raise

        return articles
