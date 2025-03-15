from fastapi import APIRouter, Query, HTTPException, Depends
from src.controllers.ranking_controller import RankingController
from src.controllers.base_controller import BaseController

ranking_router = APIRouter(prefix="/api/v1/ranking", tags=["ranking"])


def get_ranking_controller() -> RankingController:
    return RankingController()


@ranking_router.get("/news")
async def rank_news(
    ranking_type: str = Query(
        default="market_importance",
        description="Ranking strategy (market_importance, sentiment)",
    ),
    limit: int = Query(default=10, description="Number of top articles to return"),
    controller: RankingController = Depends(get_ranking_controller),
):
    """
    Get ranked financial news based on specified strategy
    """
    try:
        # Get ranked articles
        ranked_articles = controller.rank_news(ranking_type=ranking_type)

        # Apply limit
        limited_results = ranked_articles[:limit]

        return {
            "message": f"Successfully ranked using {ranking_type} strategy",
            "count": len(limited_results),
            "ranking_strategy": ranking_type,
            "data": limited_results,
        }

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ranking failed: {str(e)}")
