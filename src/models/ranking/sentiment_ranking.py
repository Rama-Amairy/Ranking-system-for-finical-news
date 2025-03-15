from .base_ranking import RankingBase
import pandas as pd


class RankBySentiment(RankingBase):
    """
    Ranks news articles by sentiment type.
    """

    def rank(self, df: pd.DataFrame) -> pd.DataFrame:
        sentiment_order = {"NEGATIVE": 1, "POSITIVE": 2, "NEUTRAL": 3}
        df["sentiment_rank"] = df["sentiment"].map(sentiment_order)
        return df.sort_values(by="sentiment_rank")
