"""
load_and_test_mysql.py
This script performs:
1. MySQL connection test
2. Data loading from eda_cleaned.csv into the MySQL database
"""
import os
import pandas as pd
import mysql.connector
from mysql.connector import Error
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Constants
CSV_PATH = 'data/csv/eda_cleaned.csv'
DB_NAME = 'imdb_movies'
TABLE_NAME = 'cleaned_movies'

# Function: Test MySQL Connection
def test_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Leo@root',
            database=DB_NAME
        )
        if connection.is_connected():
            logging.info('Connection to MySQL successful.')
            db_info = connection.get_server_info()
            logging.info(f'MySQL Server version: {db_info}')
            return True
    except Error as e:
        logging.error(f'Error while connecting to MySQL: {e}')
        return False
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            logging.info('MySQL connection closed.')

# Function: Load Data to MySQL
def load_data_to_mysql():
    if not os.path.exists(CSV_PATH):
        logging.error(f'CSV file not found at: {CSV_PATH}')
        return

    df = pd.read_csv(CSV_PATH)
    logging.info(f'DataFrame loaded from {CSV_PATH}. Shape: {df.shape}')

    required_columns = {'Movie_Name', 'Rating', 'Voting_Counts', 'Genre', 'Duration'}
    if not required_columns.issubset(df.columns):
        logging.error(f'Missing required columns. Expected: {required_columns}')
        return

    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Leo@root',
            database=DB_NAME
        )
        cursor = conn.cursor()
        logging.info(f'Connected to MySQL database: {DB_NAME}')
    except mysql.connector.Error as err:
        logging.error(f'MySQL connection failed: {err}')
        return

    try:
        cursor.execute(f'TRUNCATE TABLE {TABLE_NAME}')
        logging.info(f'Table "{TABLE_NAME}" truncated successfully.')
    except mysql.connector.Error as err:
        logging.error(f'Error truncating table "{TABLE_NAME}": {err}')
        cursor.close()
        conn.close()
        return

    insert_query = """
        INSERT INTO cleaned_movies
        (Movie_Name, Rating, Voting_Counts, Genre, Duration)
        VALUES (%s, %s, %s, %s, %s)
    """

    data = [
        (
            row['Movie_Name'],
            float(row['Rating']) if not pd.isna(row['Rating']) else None,
            int(row['Voting_Counts']) if not pd.isna(row['Voting_Counts']) else 0,
            row['Genre'],
            row['Duration']
        )
        for _, row in df.iterrows()
    ]

    try:
        cursor.executemany(insert_query, data)
        conn.commit()
        logging.info(f'Successfully inserted {cursor.rowcount} rows into "{TABLE_NAME}".')
    except mysql.connector.Error as err:
        logging.error(f'Error inserting data: {err}')
    finally:
        cursor.close()
        conn.close()
        logging.info('MySQL connection closed.')

# Main Execution
if __name__ == '__main__':
    if test_connection():
        load_data_to_mysql()
