import mysql.connector
import time

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = ''
DB_NAME = 'uworld'
TABLE_NAME = 'passage'

def get_or_create_passage_id(title, content, subject, question_count, topic):
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    query = "SELECT id FROM passage WHERE title = %s AND subject = %s"
    cursor.execute(query, (title, subject))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.close()
        connection.close()
        return result[0]
    else:
        insert_query = """
            INSERT INTO passage (title, content, subject, question_count, topic)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (title, content, subject, question_count, topic))
        passage_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        return passage_id

def get_or_create_question_id(text, correct_answer, passage_id, explanations):
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    query = "SELECT id FROM question_and_explanation WHERE text = %s AND passage_id = %s"
    cursor.execute(query, (text, passage_id))
    result = cursor.fetchone()
    
    if result and result[0] > 0:
        cursor.close()
        connection.close()
        return result[0]
    else:
        insert_query = """
            INSERT INTO question_and_explanation (text, correct_answer, passage_id, explanations)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (text, correct_answer, passage_id, explanations))
        question_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        return question_id


def get_or_create_answer_choice_id(text, question_id):
    connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
    cursor = connection.cursor()

    query = "SELECT id FROM answer_choices WHERE text = %s AND question_id = %s"
    cursor.execute(query, (text, question_id))
    result = cursor.fetchone()

    if result and result[0] > 0:
        cursor.close()
        connection.close()
        return result[0]
    else:
        insert_query = """
            INSERT INTO answer_choices (text, question_id)
            VALUES (%s, %s)
        """
        cursor.execute(insert_query, (text, question_id))
        answer_choice_id = cursor.lastrowid
        connection.commit()
        cursor.close()
        connection.close()
        return answer_choice_id