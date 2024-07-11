#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

from models import storage
from models.user import User
from models.tweet import Tweet

def clear_database():
    """Delete all records from the database tables for User and Tweet."""
    # Reload the storage to ensure session is set up
    storage.reload()
    
    # Delete all users
    all_users = storage.all(User)
    for user in all_users.values():
        storage.delete(user)
    
    # Delete all tweets
    all_tweets = storage.all(Tweet)
    for tweet in all_tweets.values():
        storage.delete(tweet)
    
    # Save the changes to the database
    storage.save()
    
    # Close the storage session
    storage.close()

if __name__ == "__main__":
    clear_database()
    print("Database cleared.")
