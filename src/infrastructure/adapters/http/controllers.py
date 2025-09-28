from fastapi import APIRouter, Depends, status, HTTPException
from src.domain.services import UrlService
from src.infrastructure.adapters.http.dependencies import get_url_service

from fastapi.responses import RedirectResponse

from src.infrastructure.adapters.http.schemas import (
    CreateShortUrlRequest,
    CreateShortUrlResponse,
)

router = APIRouter()


@router.post(
    "/urls", response_model=CreateShortUrlResponse, status_code=status.HTTP_201_CREATED
)
async def create_short_url(
    body: CreateShortUrlRequest, service: UrlService = Depends(get_url_service)
):
    """
    Create a new shortened URL.

    Args:
        body (CreateShortUrlRequest): The request payload with the original URL.
        service (UrlService): The URL service dependency.

    Returns:
        CreateShortUrlResponse: The response containing the original URL and its short code.
    """
    url = await service.create_short_url(str(body.url))

    return CreateShortUrlResponse(
        original_url=url.original_url, short_code=url.short_code
    )


@router.get("/{short_code}")
async def redirect(short_code: str, service: UrlService = Depends(get_url_service)):
    """
    Redirect to the original URL for a given short code.

    Args:
        short_code (str): The short code to resolve.
        service (UrlService): The URL service dependency.

    Returns:
        RedirectResponse: A redirect response to the original URL.
    """
    try:
        original_url = await service.get_original_url(short_code=short_code)
        return RedirectResponse(
            url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except ValueError as err:
        raise HTTPException(status_code=404, detail=str(err))
