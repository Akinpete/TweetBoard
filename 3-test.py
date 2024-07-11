#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

from models import storage
from models.user import User
from models.tweet import Tweet

# Reload the storage to ensure session is set up
storage.reload()

# Query all users
all_users = storage.all(User)
print("All users:")
for key, user in all_users.items():
    print(user)

# Query all tweets
all_tweets = storage.all(Tweet)
print("All tweets:")
for key, tweet in all_tweets.items():
    print(tweet)

# Query specific user by username
username_to_search = "California"
user_found = None
users = storage.all(User)
for user in users.values():
    if user.username == username_to_search:
        user_found = user
        print(f"User found: {user}")
        break

if user_found:
    # Query tweets by the found user
    user_id_to_search = user_found.id
    tweets = storage.all(Tweet)
    print(f"All tweets by user with ID {user_id_to_search}:")
    for tweet in tweets.values():
        if tweet.user_id == user_id_to_search:
            print(tweet)
else:
    print(f"No user found with username {username_to_search}")

# Close the storage session
storage.close()
