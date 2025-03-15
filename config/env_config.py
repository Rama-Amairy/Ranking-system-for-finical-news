from pydantic_settings import BaseSettings, SettingsConfigDict

# in this classes you have to be sure to name them in the same way in the pydantic (Settings and Config)


class Settings(BaseSettings):

    APP_NAME: str
    APP_VERSION: str
    NEWS_API_KEY: str

    # Add the .env file without any white spaces also ensure no spacing in .env file.
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


def get_settings():
    return Settings()
