from dataclasses import dataclass


@dataclass
class Url:
    """
    Data model representing a shortened URL entry.

    Attributes
    ----------
    original_url : str
        The full, original URL before shortening.
    short_code : str
        The unique short code used to reference the original URL.
    """

    original_url: str
    short_code: str
