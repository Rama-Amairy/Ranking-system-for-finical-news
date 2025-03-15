import pandas as pd
from src.controllers.base_controller import BaseController


from src.models.ranking.financial_impact_ranking import FinancialImpactRanking
from src.models.ranking.sentiment_ranking import RankBySentiment


class RankingController(BaseController):
    """
    Controller for ranking news articles using different strategies.
    """

    def __init__(self):
        """
        Initializes the RankingController.

        Args:
            file_path (str): Path to the CSV file containing processed news.
        """
        super().__init__()
        self.file_path = self.processed_data_path
        self.rankers = {
            "market_importance": FinancialImpactRanking(),
            "sentiment": RankBySentiment(),
        }

    def load_news(self):
        """
        Loads processed news articles from a CSV file.

        Returns:
            pd.DataFrame: DataFrame containing news articles.
        """
        try:
            return pd.read_csv(self.file_path)
        except Exception as e:
            print(f"Error loading news data: {e}")
            return None

    def rank_news(self, ranking_type="market_importance", limit: int = None):
        """
        Enhanced with limit handling
        """
        df = self.load_news()
        if df is None or df.empty:
            return []

        if ranking_type not in self.rankers:
            raise ValueError(
                f"Invalid ranking type: {ranking_type}. "
                f"Available types: {list(self.rankers.keys())}"
            )

        ranked_df = self.rankers[ranking_type].rank(df)

        # Convert to records before limiting
        results = ranked_df.to_dict(orient="records")

        return results[:limit] if limit else results
