#!/usr/bin/python3

import json
from handle_json import classify_tweet_content
from get_token import get_token
from form_url import build_url, get_tweet_data

def tweet_type(tweet_id):
    """
    Determine the type of content in a tweet using its ID.

    Args:
        tweet_id (str): The ID of the tweet.

    Returns:
        str: The classified content of the tweet.
    """
    url=build_url(tweet_id, get_token(tweet_id))
    json_data = get_tweet_data(url)

    # Check if json_data is already a dictionary
    if isinstance(json_data, dict):
        tweet_data = json_data
    else:
        # If it's a string, parse it into a dictionary
        try:
            tweet_data = json.loads(json_data)
        except json.JSONDecodeError:
            print("Error: Invalid JSON data")
            exit(1)

    check = classify_tweet_content(tweet_data)
    return check

def safe_get_video_url(variants, index=1):
    """
    Safely retrieve a video URL from a list of video variants
    gotten from json data

    Args:
        variants (list): A list of video variant dictionaries.
        index (int, optional): The index of the video variant to retrieve. Defaults to 1.

    Returns:
        str or None: The video URL if available, otherwise None.
    """
    if variants is None:
        return None
    else:
        try:
            return variants[index].get('video_url')
        except (IndexError, AttributeError):
            return None
    
       
        