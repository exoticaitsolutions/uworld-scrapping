import mysql.connector
import time

# Database configuration
DB_HOST = 'localhost'       # e.g., 'localhost'
DB_USER = 'root'       # e.g., 'root'
DB_PASSWORD = ''  # e.g., 'your_password'
DB_NAME = 'uworld_database'       # e.g., 'uworld_db'
TABLE_NAME = 'passage'               # Table name in your database


db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'localhost',
    'database': 'your_database'
}


def db_config():         
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        
    # Create a cursor object
    cursor = connection.cursor()
    return cursor

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



def get_or_create_passage_id(title, content, subject, question_count, topic):
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    # Check if the passage already exists
    query = "SELECT id FROM passage WHERE title = %s AND subject = %s"
    cursor.execute(query, (title, subject))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        # Passage already exists, return its ID
        cursor.close()
        connection.close()
        return result[0]
    else:
        # Passage doesn't exist, insert a new passage and return its ID
        insert_query = """
            INSERT INTO passage (title, content, subject, question_count, topic)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (title, content, subject, question_count, topic))
        passage_id = cursor.lastrowid  # Store the last inserted ID
        connection.commit()  # Commit the transaction
        cursor.close()
        connection.close()
        return passage_id

def get_or_create_question_id(text, correct_answer, passage_id, explanations):
    # Establish database connection
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    # Check if the question already exists
    query = "SELECT id FROM question_and_explanation WHERE text = %s AND passage_id = %s"
    cursor.execute(query, (text, passage_id))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        # Question already exists, return its ID
        cursor.close()
        connection.close()
        return result[0]
    else:
        # Question doesn't exist, insert a new question and return its ID
        insert_query = """
            INSERT INTO question_and_explanation (text, correct_answer, passage_id, explanations)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (text, correct_answer, passage_id, explanations))
        question_id = cursor.lastrowid  # Store the last inserted ID
        connection.commit()  # Commit the transaction
        cursor.close()
        connection.close()
        return question_id


def get_or_create_answer_choice_id(text, question_id):
    # Establish database connection
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    # Check if the answer choice already exists
    query = "SELECT id FROM answer_choices WHERE text = %s AND question_id = %s"
    cursor.execute(query, (text, question_id))
    result = cursor.fetchone()

    if result and result[0] > 0:
        # Answer choice already exists, return its ID
        cursor.close()
        connection.close()
        return result[0]
    else:
        # Answer choice doesn't exist, insert a new answer choice and return its ID
        insert_query = """
            INSERT INTO answer_choices (text, question_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (text, question_id))
        answer_choice_id = cursor.lastrowid  # Store the last inserted ID
        connection.commit()  # Commit the transaction
        cursor.close()
        connection.close()
        return answer_choice_id