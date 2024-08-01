import math

def get_token(id: str) -> str:
    """
    Generate a token from a given tweetID using mathematical operations and base conversion.

    Args:
        id (str): The tweetID to be converted into a token.

    Returns:
        str: The generated token in base 36 format with all zeros and the decimal point removed.
    """
    # Convert to number and perform calculation
    result = (int(id) / 1e15) * math.pi
    print(f"Intermediate result: {result}")

    # Convert to base 36 string, replicating JavaScript's toString(36) behavior
    base_36 = ""
    scale = 10**20  # Increase precision
    scaled_result = int(result * scale)
    
    while scaled_result > 0:
        scaled_result, remainder = divmod(scaled_result, 36)
        base_36 = "0123456789abcdefghijklmnopqrstuvwxyz"[remainder] + base_36

    # Insert the decimal point
    decimal_position = len(base_36) - 20
    if decimal_position > 0:
        base_36 = base_36[:decimal_position] + '.' + base_36[decimal_position:]
    else:
        base_36 = '0.' + '0' * (-decimal_position) + base_36

    print(f"Base 36 representation: {base_36}")

    # Remove zeros and decimal point
    token = base_36.replace('0', '').replace('.', '')
    return token

if __name__ == '__main__':
    # Test with the given tweet ID
    # tweet_id = "1797955993718186006"
    tweet_id = "1812849402177863844"
    
    token = get_token(tweet_id)
    print(f"Final token for tweet ID {tweet_id}: {token}")