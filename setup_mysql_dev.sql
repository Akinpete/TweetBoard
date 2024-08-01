-- Prep MySQL server for the project
CREATE DATABASE IF NOT EXISTS test_bookmarks_db;
CREATE USER IF NOT EXISTS 'peter_dev'@'localhost' IDENTIFIED BY 'peter_dev_pwd';
GRANT ALL PRIVILEGES ON test_bookmarks_db .* TO 'peter_dev'@'localhost';
GRANT SELECT ON performance_schema .* TO 'peter_dev'@'localhost';
FLUSH PRIVILEGES;

-- echo "SHOW DATABASES;" | mysql -utube_dev -p | grep tube_dev_db

-- echo "SHOW GRANTS FOR 'tube_dev'@'localhost';" | mysql -uroot -p