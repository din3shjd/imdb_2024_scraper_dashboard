"""
merge_csv_files.py
Merges all genre-wise CSV files in data/csv/ into a single cleaned dataset.
Output: data/csv/cleaned_movies.csv """
import os
import pandas as pd
import logging
from typing import List

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Constants
CSV_DIR = os.path.join('data', 'csv')
OUTPUT_PATH = os.path.join(CSV_DIR, 'cleaned_movies.csv')

# Get All Genre Files
def get_genre_csv_files(directory: str) -> List[str]:
    return [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.endswith('_movies.csv')
    ]

# Merge CSV Files
def merge_genre_csv_files(input_dir: str = CSV_DIR, output_file: str = OUTPUT_PATH):
    logging.info(f'Scanning directory: {input_dir}')
    
    genre_files = get_genre_csv_files(input_dir)
    if not genre_files:
        logging.warning('No genre-specific CSV files found to merge.')
        return

    dataframes = []
    for file in genre_files:
        logging.info(f'Reading file: {file}')
        df = pd.read_csv(file)
        dataframes.append(df)

    merged_df = pd.concat(dataframes, ignore_index=True)
    logging.info(f'Total combined rows before deduplication: {len(merged_df)}')

    merged_df.drop_duplicates(subset=['Movie_Name'], inplace=True)
    merged_df.to_csv(output_file, index=False)

    logging.info(f'Merged data saved to: {output_file}')
    logging.info(f'Final row count after removing duplicates: {len(merged_df)}')

# Script Entry Point
if __name__ == '__main__':
    merge_genre_csv_files()
