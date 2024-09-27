import mysql.connector
import time

# Database configuration
DB_HOST = 'localhost'       # e.g., 'localhost'
DB_USER = 'root'       # e.g., 'root'
DB_PASSWORD = ''  # e.g., 'your_password'
DB_NAME = 'uworld'       # e.g., 'uworld_db'
TABLE_NAME = 'passage'               # Table name in your database


def insert_data_into_mysql(data):
    try:
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
        # Create a cursor object
        cursor = connection.cursor()
        
        # SQL query to insert data into the `passage` table
        insert_query = f"""
            INSERT INTO {TABLE_NAME} (id, title, content, subject, question_count, topic)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        
        # Iterate over each item in the data list and insert it into the table
        for entry in data:
            cursor.execute(
                insert_query,
                (
                    entry["id"],
                    entry["title"],
                    entry["content"],
                    entry["subject"],
                    entry["question_count"],
                    entry["topic"]
                )
            )
        
        # Commit the transaction to save changes
        connection.commit()
        print("Data inserted successfully into the table.")
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    
    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("MySQL connection closed.")