from fastapi import FastAPI
from src.routes import base, news

# from src.helpers.log_helper import Logger  # Import your Logger helper


# Initialize logger
# log_instance = Logger(log_name="app")
# logger = log_instance.get_logger()

app = FastAPI(title="Financial News Ranking API")

# Register API routes
app.include_router(base.base_router)
app.include_router(news.news_router)

# logger.info("FastAPI application has started.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
