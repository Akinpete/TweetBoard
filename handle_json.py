def classify_tweet_content(json_data):
    """
    Classify the content of a tweet based on its media type.

    Args:
        json_data (dict): The JSON data of a tweet.

    Returns:
        dict or str: A dictionary with classified tweet information, or "unknown" if classification fails.
    """
    # Helper functions
    def is_only_text(tweet):
        """
        Determine if the tweet contains only text, without any media.

        Args:
            tweet (dict): The tweet JSON data.

        Returns:
            bool: True if the tweet contains only text, False otherwise.
        """
        return (
            'media' not in tweet.get('entities', {}) and
            not tweet.get('mediaDetails') and
            not tweet.get('photos') and
            'video' not in tweet
        )

    def has_image(tweet):
        """
        Check if the tweet contains an image.

        Args:
            tweet (dict): The tweet JSON data.

        Returns:
            bool: True if the tweet contains an image, False otherwise.
        """
        return (
            any(m.get('type') == 'photo' for m in tweet.get('entities', {}).get('media', [])) or
            any(m.get('type') == 'photo' for m in tweet.get('mediaDetails', [])) or
            tweet.get('photos')
        )

    def has_video(tweet):
        """
        Check if the tweet contains a video.

        Args:
            tweet (dict): The tweet JSON data.

        Returns:
            bool: True if the tweet contains a video, False otherwise.
        """
        return (
            any(m.get('type') == 'video' for m in tweet.get('entities', {}).get('media', [])) or
            any(m.get('type') == 'video' for m in tweet.get('mediaDetails', [])) or
            'video' in tweet
        )
        
    def extract_common_info(tweet):
        """
        Extract common information from a tweet.

        Args:
            tweet (dict): The tweet JSON data.

        Returns:
            dict: A dictionary containing common tweet information.
        """
        return {
            "profile_image_url": tweet.get('user', {}).get('profile_image_url_https'),
            "tweet_link": tweet.get('id_str'),
            "text": tweet.get('text'),
            "name": tweet.get('user', {}).get('name'),
            "screen_name": tweet.get('user', {}).get('screen_name'),
            "created_at": tweet.get('created_at'),
            "favorite_count": tweet.get('favorite_count'),
            "conversation_count": tweet.get('conversation_count'),
            "hashtags": [hashtag['text'] for hashtag in tweet.get('entities', {}).get('hashtags', [])],
            "user_mentions": [
                {
                    "name": mention['name'],
                    "screen_name": mention['screen_name']
                } for mention in tweet.get('entities', {}).get('user_mentions', [])
            ]
        }
        
    
        
# Main classification logic
    if is_only_text(json_data):
        return {
            "type": "text",
            "profile_image_url": json_data.get('user', {}).get('profile_image_url_https'),
            "text": json_data.get('text'),
            "name": json_data.get('user', {}).get('name'),
            "screen_name": json_data.get('user', {}).get('screen_name')
        }
    elif has_image(json_data) and not has_video(json_data):
        image_info = json_data.get('photos', [{}])[0] if json_data.get('photos') else json_data.get('mediaDetails', [{}])[0]
        return {
            "type": "image",
            **extract_common_info(json_data),
            "image_url": image_info.get('url') or image_info.get('media_url_https'),
            "image_width": image_info.get('width'),
            "image_height": image_info.get('height')
        }
        
    elif has_video(json_data):
        video_info = json_data.get('video', {})
        media_details = json_data.get('mediaDetails', [{}])[0]
        return {
            "type": "video",
            **extract_common_info(json_data),
            "video_duration_ms": video_info.get('durationMs'),
            "video_aspect_ratio": video_info.get('aspectRatio'),
            "video_poster": video_info.get('poster'),
            "video_variants": [
                {
                    "type": variant.get('type'),
                    "video_url": variant.get('src')
                } for variant in video_info.get('variants', [])
            ],
            "video_view_count": video_info.get('viewCount'),
            "video_width": media_details.get('original_info', {}).get('width'),
            "video_height": media_details.get('original_info', {}).get('height')
        }
    else:
        return "unknown"