import yaml
from pydantic import BaseModel, Field
from typing import List


class AppConfigModel(BaseModel):
    """
    Pydantic model for validating application settings from YAML.
    """

    name: str = Field(..., description="Application name")
    version: str = Field(..., description="Application version")


class NewsConfigModel(BaseModel):
    """
    Pydantic model for validating news-related configurations.
    """

    query_url: str = Field(..., description="URL for query-based news search")
    allowed_queries: List[str] = Field(
        ..., description="List of allowed finance-related queries"
    )


class SentimentConfigModel(BaseModel):
    """
    Pydantic model for validating sentiment analysis model configurations.
    """

    name: str = Field(..., description="Name of the sentiment analysis model")
    max_length: int = Field(
        512, description="Maximum number of tokens for sentiment analysis"
    )


class ModelsConfig(BaseModel):
    """
    Pydantic model for validating the models section.
    """

    sentiment_analysis_model: SentimentConfigModel


class ConfigModel(BaseModel):
    """
    Root Pydantic model for validating the entire configuration file.
    """

    app: AppConfigModel
    news: NewsConfigModel
    models: ModelsConfig


def load_config(file_path="config/config.yaml") -> ConfigModel:
    """
    Reads and validates YAML configuration file using Pydantic.

    Args:
        file_path (str): Path to the YAML config file.

    Returns:
        ConfigModel: Validated configuration model.
    """
    with open(file_path, "r") as file:
        raw_config = yaml.safe_load(file)
    return ConfigModel(**raw_config)


# Load and validate configuration
app_config = load_config()
