import requests

def build_url(tweet_id, token):
    """
    Construct the URL to access tweet data using a tweet ID and token.

    Args:
        tweet_id (str): The ID of the tweet to access.
        token (str): The token required to authenticate the request.

    Returns:
        str: The complete URL for accessing the tweet data.
    """
    base_url = "https://cdn.syndication.twimg.com/tweet-result"
    return f"{base_url}?id={tweet_id}&lang=en&token={token}"

def get_tweet_data(url):
    """
    Retrieve tweet data from a given URL.

    Args:
        url (str): The URL to fetch tweet data from.

    Returns:
        dict or None: The JSON data of the tweet if the request is successful, None otherwise.
    """
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to get data for URL {url}. Status code: {response.status_code}")
        return None
