import pandas as pd
from abc import ABC, abstractmethod


class RankingBase(ABC):
    """
    Abstract base class for ranking news articles.
    """

    @abstractmethod
    def rank(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ranks news articles based on specific criteria.
        """
        pass
