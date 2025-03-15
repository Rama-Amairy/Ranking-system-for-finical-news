from src.controllers.base_controller import BaseController
import pandas as pd
import os
import ast  # For safely evaluating string representations of dictionaries
import re  # For cleaning up content
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
        processed_articles = []
        for article in news:
            try:
                # Skip if article is not a dictionary
                if not isinstance(article, dict):
                    # logger.warning
                    print(f"Skipping invalid article: {article}")
                    continue

                # Extract and clean fields
                title = article.get("title", "No Title").strip()
                description = article.get("description", "").strip()
                content = article.get("content", "").strip()

                # Clean up content (remove metadata like [+4155 chars])
                content = re.sub(r"\[\+\d+ chars\]", "", content).strip()

                # Parse the source field (string representation of a dictionary)
                source = article.get("source", "{}")
                try:
                    source_dict = ast.literal_eval(
                        source
                    )  # Safely evaluate the string as a dictionary
                    source_name = source_dict.get("name", "unknown")
                except (ValueError, SyntaxError):
                    source_name = "unknown"

                # Build the processed article
                processed_articles.append(
                    {
                        "title": title,
                        "content": content,
                        "description": description,
                        "text": f"{description} {content}".strip(),
                        "publishedAt": article.get("publishedAt", ""),
                        "source": source_name,
                        "url": article.get("url", ""),
                        "sentiment_label": article.get("sentiment_label", "NEUTRAL"),
                        "sentiment_score": float(article.get("sentiment_score", 0)),
                    }
                )
            except Exception as e:
                # logger.error
                print(f"Error processing article: {e}")
                continue

        if not processed_articles:
            print("No valid articles found after processing.")

        return processed_articles

    def save_raw_data(self, raw_articles: list[dict], file_path: str = None) -> str:
        """
        Saves raw news articles into a CSV file.

        Args:
            raw_articles (list[dict]): A list of raw news articles.
            file_path (str, optional): The file path to save the CSV file. Defaults to self.raw_data_path.

        Returns:
            str: Success or failure message.
        """
        if not raw_articles:
            return Messages.FETCH_FAILURE.value

        file_path = file_path or self.raw_data_path

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(raw_articles)

            # Save DataFrame to CSV
            df.to_csv(file_path, index=False, encoding="utf-8")
            return Messages.FETCH_SUCCESS.value
        except Exception as e:
            # Log the error if needed
            return Messages.FETCH_FAILURE.value

    def read_raw_data(self, file_path: str = None) -> list[dict]:
        """
        Reads raw news articles from a CSV file.

        Args:
            file_path (str, optional): The file path to read the CSV file. Defaults to self.raw_data_path.

        Returns:
            list[dict]: A list of raw news articles.
        """
        file_path = file_path or self.raw_data_path

        try:
            # Read CSV file into DataFrame
            df = pd.read_csv(file_path)

            # Convert DataFrame to list of dictionaries
            return df.to_dict("records")
        except Exception as e:
            # Log the error if needed
            return []

    def save_processing_data(
        self,
        processed_articles: list[dict],
        file_path: str = None,
    ) -> str:
        """
        Saves the processed news articles into a CSV file.

        Args:
            processed_articles (list[dict]): A list of processed news articles.
            file_path (str, optional): The file path to save the CSV file. Defaults to self.processed_data_path.

        Returns:
            str: Success or failure message.
        """
        if not processed_articles:
            return Messages.PROCESS_FAILURE.value

        file_path = file_path or self.processed_data_path

        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Convert list of dictionaries to DataFrame
            df = pd.DataFrame(processed_articles)

            # Save DataFrame to CSV
            df.to_csv(file_path, index=False, encoding="utf-8")
            return Messages.PROCESS_SUCCESS.value
        except Exception as e:
            # Log the error if needed
            return Messages.PROCESS_FAILURE.value

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
            # Log the error if needed
            raise

        return articles
