import MySQLdb
import sys

def test_mysql_connection(host, user, password, database):
    try:
        # Attempt to establish a connection
        connection = MySQLdb.connect(
            host=host,
            user=user,
            passwd=password,
            db=database
        )
        
        print("Successfully connected to the database!")
        
        # If connection successful, try to execute a simple query
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"Database version: {version[0]}")
        
        connection.close()
        print("Connection closed successfully.")
        
    except MySQLdb.Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        print("Error details:")
        print(f"Error code: {e.args[0]}")
        print(f"Error message: {e.args[1]}")
        
        # Additional error handling suggestions
        if e.args[0] == 1045:  # Access denied error
            print("Suggestion: Double-check your username and password.")
            print("Make sure the user 'tweetbox_dev' has the correct permissions.")
        elif e.args[0] == 2003:  # Can't connect to MySQL server
            print("Suggestion: Verify that the MySQL server is running and that the hostname is correct.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print(f"Error type: {type(e).__name__}")

if __name__ == "__main__":
    # Replace these with your actual database credentials
    HOST = "localhost"
    USER = "tweetbox_dev"
    PASSWORD = "tweetbox_dev_pwd"
    DATABASE = "tweetbox_dev_db"

    test_mysql_connection(HOST, USER, PASSWORD, DATABASE)