import os
import pandas as pd
import mysql.connector
import warnings

# Suppress specific pandas warnings
warnings.filterwarnings("ignore", message="pandas only supports SQLAlchemy connectable")


# Step 1: Establish a connection to the database
connection = mysql.connector.connect(
    host='localhost',    
    user='root',           
    password='',            
    database='uworld' 
)

# Step 2: Get the unique subjects from the passage table
unique_subject_query = "SELECT DISTINCT subject FROM passage"
unique_subjects_df = pd.read_sql(unique_subject_query, connection)
unique_subjects = unique_subjects_df['subject'].tolist()
print("unique_subjects : ", unique_subjects)

# Step 3: Create a base directory to store all the subject folders
base_dir = 'Subject_Folders'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

# Step 4: Loop through each unique subject and create CSV files in respective folders
for subject in unique_subjects:
    # Create a directory for the subject
    subject_dir = os.path.join(base_dir, subject)
    if not os.path.exists(subject_dir):
        os.makedirs(subject_dir)
    
    # Query passage table for the current subject
    passage_query = f"SELECT * FROM passage WHERE subject = '{subject}'"
    passage_df = pd.read_sql(passage_query, connection)
    passage_csv_path = os.path.join(subject_dir, 'passages.csv')     
    passage_df.to_csv(passage_csv_path, index=False)
    
    # Get passage IDs for the current subject and ensure they are integers
    passage_ids = list(passage_df['id'].astype(int).values)  # Convert to plain int
    passage_ids_str = ', '.join(map(str, passage_ids))  # Convert to string for SQL query

    # Query questions table using passage IDs
    question_query = f"SELECT * FROM question_and_explanation WHERE passage_id IN ({passage_ids_str})"
    question_df = pd.read_sql(question_query, connection)
    question_csv_path = os.path.join(subject_dir, 'questions.csv')
    question_df.to_csv(question_csv_path, index=False)

    # Get question IDs for the current passage IDs
    question_ids = list(question_df['id'].astype(int).values)  # Convert to plain int
    question_ids_str = ', '.join(map(str, question_ids))  # Convert to string for SQL query

    # Query answers table using question IDs
    answer_query = f"SELECT * FROM answer_choices WHERE question_id IN ({question_ids_str})"
    answer_df = pd.read_sql(answer_query, connection)
    answer_csv_path = os.path.join(subject_dir, 'answers.csv')
    answer_df.to_csv(answer_csv_path, index=False)

    print(f"Data saved for subject: {subject} in folder: {subject_dir}")

# Close the database connection
connection.close()
            