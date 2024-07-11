#!/usr/bin/python3

import os
import sys

parent_dir = r"C:\Users\User\Documents\VS CODE - 2024\Foundations Portfolio Presentation\Tweet2.0"
sys.path.append(parent_dir)

from models import storage

def drop_all_tables():
    """Drop all tables in the database."""
    storage.drop_all_tables()

if __name__ == "__main__":
    drop_all_tables()
