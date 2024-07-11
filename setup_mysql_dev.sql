-- Prep MySQL server for the project
CREATE DATABASE IF NOT EXISTS tweetbox_dev_db;
CREATE USER IF NOT EXISTS 'tweetbox_dev'@'localhost' IDENTIFIED BY 'tweetbox_dev_pwd';
GRANT ALL PRIVILEGES ON tweetbox_dev_db .* TO 'tweetbox_dev'@'localhost';
GRANT SELECT ON performance_schema .* TO 'tweetbox_dev'@'localhost';
FLUSH PRIVILEGES;

-- echo "SHOW DATABASES;" | mysql -utweetbox_dev -p | grep tweetbox_dev_db

-- echo "SHOW GRANTS FOR 'tweetbox_dev'@'localhost';" | mysql -uroot -p