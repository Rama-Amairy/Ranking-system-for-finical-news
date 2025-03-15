from enum import Enum


class Messages(Enum):
    FETCH_SUCCESS = "Successfully fetched news articles."
    FETCH_FAILURE = "Failed to fetch news articles."
    PROCESS_SUCCESS = "News processed and saved successfully."
    PROCESS_FAILURE = "Error occurred while processing news."
    MODEL_PREDICTION_FAILURE = "Sentiment prediction failed."
