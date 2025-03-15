import pandas as pd
import re
from textblob import TextBlob
from .base_ranking import RankingBase


class FinancialImpactRanking(RankingBase):
    """
    Ranks news articles based on potential market impact factors:
    - Sentiment strength and polarity
    - Key financial entity mentions
    - Market-moving verb detection
    - Content novelty score
    - Source credibility weighting
    """

    def __init__(self):
        self.market_verbs = {
            "acquire",
            "merge",
            "launch",
            "cut",
            "raise",
            "lower",
            "approve",
            "reject",
            "investigate",
            "settle",
            "expand",
            "reduce",
            "forecast",
            "warn",
            "outperform",
            "downgrade",
        }

        self.financial_entities = {
            "stocks",
            "bonds",
            "federal reserve",
            "interest rates",
            "inflation",
            "gdp",
            "earnings",
            "dividend",
            "ipo",
            "buyback",
        }

    def rank(self, df: pd.DataFrame) -> pd.DataFrame:
        # Calculate impact factors
        df = df.assign(
            sentiment_strength=df["text"].apply(self._calculate_sentiment_strength),
            entity_density=df["text"].apply(self._calculate_entity_density),
            market_verbs=df["text"].apply(self._count_market_verbs),
            novelty_score=df["text"].apply(self._calculate_novelty),
            source_credibility=df["source"].apply(self._source_weight),
        )

        # Normalize scores
        for col in [
            "sentiment_strength",
            "entity_density",
            "market_verbs",
            "novelty_score",
        ]:
            df[col] = df[col].rank(pct=True)

        # Composite impact score
        df["market_impact"] = (
            df["sentiment_strength"] * 0.3
            + df["entity_density"] * 0.25
            + df["market_verbs"] * 0.2
            + df["novelty_score"] * 0.15
            + df["source_credibility"] * 0.1
        )

        return df.sort_values(by="market_impact", ascending=False)

    def _calculate_sentiment_strength(self, text: str) -> float:
        """Measure both polarity and intensity of sentiment"""
        analysis = TextBlob(text)
        return abs(analysis.sentiment.polarity) * analysis.sentiment.subjectivity

    def _calculate_entity_density(self, text: str) -> int:
        """Count mentions of key financial terms and companies"""
        text_lower = text.lower()
        return sum(
            1 for entity in self.financial_entities if entity in text_lower
        ) + len(
            re.findall(r"\b[A-Z]{2,}\b", text)
        )  # Stock tickers

    def _count_market_verbs(self, text: str) -> int:
        """Identify action verbs that typically move markets"""
        return sum(
            1
            for verb in self.market_verbs
            if re.search(rf"\b{verb}[ed|s|ing]*\b", text, re.I)
        )

    def _calculate_novelty(self, text: str) -> float:
        """Measure content uniqueness using TF-IDF-like scoring"""
        # This would integrate with a historical news database
        # Placeholder implementation
        return len(set(text.split())) / len(text.split())  # Unique word ratio

    def _source_weight(self, source: str) -> float:
        """Weight by source market influence"""
        credibility_map = {
            "bloomberg": 0.95,
            "reuters": 0.93,
            "financial times": 0.90,
            "cnbc": 0.85,
            "default": 0.5,
        }
        return credibility_map.get(source.lower(), credibility_map["default"])
