#!/bin/bash

export HBNB_MYSQL_USER=tweetbox_dev
export HBNB_MYSQL_PWD=tweetbox_dev_pwd
export HBNB_MYSQL_HOST=localhost
export HBNB_MYSQL_DB=tweetbox_dev_db

python3 drop_tables_db.py
# python3 3-test.py
# python3 2-test.py
# python3 clean_database.py
# python3 main_place_amenities.py
# python3 test-review.py