from fastapi import APIRouter, HTTPException, Query
from tortoise.expressions import Q

from app.db.videos import Videos
import re

from app.utils.settings import settings

api_router = APIRouter()


@api_router.get('/')
def test_router():
    return {"detail": "Health check from api router!"}


@api_router.get('/fetch')
def fetch_results():
    return


@api_router.get('/search')
async def search_results(query: str, page: int = Query(1, ge=1)):
    page_size = settings.PAGE_SIZE
    processed_query = ' | '.join(re.findall(r'\w+', query.lower()))
    try:
        videos = await Videos.filter(
            Q(title__search=processed_query) | Q(description__search=processed_query)
        ).order_by('-id').all().values()

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


@api_router.post('/insert')
async def insert_data(title: str):
    try:
        video = await Videos.create(title=title)
        return {"message": "Data inserted successfully", "id": video.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert data: {str(e)}")
