from fastapi import APIRouter, HTTPException, Query
from tortoise.expressions import Q

from app.db.videos import Videos
import re

from app.utils.settings import settings

api_router = APIRouter()


@api_router.get('/fetch')
async def fetch_results(page: int = Query(1, ge=1)):
    """
    :param page:
    :return: results in dict in descending order of published_at

     Route to fetch all results in dB.

    """
    page_size = settings.PAGE_SIZE
    try:
        videos = await Videos.filter().order_by('-published_at').all().values()

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        paginated_videos = videos[start_idx:end_idx]

        return {
            "page": page,
            "page_size": page_size,
            "total_pages": (len(videos) + page_size - 1) // page_size,
            "total_results": len(videos),
            "results": paginated_videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")


@api_router.get('/search')
async def search_results(query: str, page: int = Query(1, ge=1)):
    """
    :param query:
    :param page: results in dict in descending order of published_at
    :return:
    """
    page_size = settings.PAGE_SIZE
    processed_query = ' | '.join(re.findall(r'\w+', query.lower()))
    try:
        videos = await Videos.filter(
            Q(title__search=processed_query) | Q(description__search=processed_query)
        ).order_by('-published_at').all().values()

        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size

        paginated_videos = videos[start_idx:end_idx]

        return {
            "page": page,
            "page_size": page_size,
            "total_pages": (len(videos) + page_size - 1) // page_size,
            "total_results": len(videos),
            "results": paginated_videos
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")
