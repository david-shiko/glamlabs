from typing import List
import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
# from dependencies import Scrapper

from dependencies import scrapper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )

logger = logging.getLogger(__name__)


class PhotosIn(BaseModel):
    """Schema to validate incoming request and provide info for OpenApi"""

    username: str = Field(
        ...,
        title="Instagram Username",
        description="The username of the Instagram account you want to retrieve photos from.",
        example="elonrmuskk"
    )

    max_count: int = Field(
        ...,
        title="Maximum Count",
        description="The maximum number of photos to retrieve.",
        example=10,
        gt=0,
        lt=1000
    )


class PhotosOut(BaseModel):
    urls: List[str]


router = APIRouter()


@router.get("/getPhotos", response_model=PhotosOut, )
async def read_photos(username: str, max_count: int, ) -> PhotosOut:
    """Return URLs of Instagram photos for a given username and max count.
    Args:
    data (PhotosIn): A PhotosIn model instance containing:
        username (str): Instagram username to fetch photos from.
        max_count (int): Maximum number of photos to return.

    Returns:
    PhotosOut: A PhotosOut model instance containing list of photo URLs.
    """
    logging.info(f"Fetching photos for username: {username} with count: {max_count}")
    try:
        photos = await scrapper.get_photos(username, max_count)
        return PhotosOut(urls=photos)
    except Exception as e:
        logging.error(f"An error occurred while fetching photos: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching photos.", )
