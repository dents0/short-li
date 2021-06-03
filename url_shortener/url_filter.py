import re
from url_shortener import app


def validate_url(url=None):
    """
    Checks if the passed string is a URL
    """

    url_filter = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    # If the provided URL is shortened already
    if f"{app.config['TARGET_URL']}" in url:
        return "It seems this URL has been shortened already"

    # If URL matches the filter
    if re.search(url_filter, url) and '.' in url and url[-1] != '.':
        return True

    # If URL doesn't match the required pattern
    return "Wrong URL format"
