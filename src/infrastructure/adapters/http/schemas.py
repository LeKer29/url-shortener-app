from pydantic import BaseModel, HttpUrl


class CreateShortUrlRequest(BaseModel):
    """
    Request schema for creating a shortened URL.

    Attributes:
        url (HttpUrl): The original full URL to shorten.
    """

    url: HttpUrl


class CreateShortUrlResponse(BaseModel):
    """
    Response schema for a shortened URL.

    Attributes:
        short_code (str): The generated unique short code.
        original_url (str): The original full URL.
    """

    short_code: str
    original_url: str
