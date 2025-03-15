from transformers import pipeline
from src.models.base_model import BaseModelHandler


class SentimentModelHandler(BaseModelHandler):
    def __init__(self, model_name: str):
        super().__init__(model_name)
        self.model = None

    def load_model(self):
        """Load the sentiment analysis model using the pipeline with an increased timeout."""
        # Increase request_timeout to 60 seconds
        self.model = pipeline("sentiment-analysis", model=self.model_name)

    def predict(self, text: str):
        """
        Run sentiment analysis on the given text.
        """
        if not text.strip():
            return {"label": "Neutral", "score": 0.0}

        result = self.model(text)[0]
        return {
            "label": result.get("label", "Neutral"),
            "score": result.get("score", 0.0),
        }
