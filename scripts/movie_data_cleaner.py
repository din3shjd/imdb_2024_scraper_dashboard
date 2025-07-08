"""
movie_data_cleaner.py
Cleans and enhances the cleaned_movies.csv by:
- Converting 'Duration_Total' (e.g., '2h 10m') to total minutes
- Categorizing duration into display and filter buckets
- Converting 'Voting_Counts' like '253K', '1.2M', or '5700.0' to integers
- Saving the cleaned data to: data/csv/cleaned_movies.csv   """
import os
import re
import pandas as pd
import numpy as np
import logging

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Helper Functions
def convert_duration_to_minutes(duration: str) -> float:
    if not isinstance(duration, str) or not duration.strip():
        return None
    hours = minutes = 0
    hour_match = re.search(r'(\d+)\s*h', duration)
    if hour_match:
        hours = int(hour_match.group(1))
    minute_match = re.search(r'(\d+)\s*m', duration)
    if minute_match:
        minutes = int(minute_match.group(1))
    return hours * 60 + minutes if hours or minutes else None

def categorize_duration(minutes: float) -> str:
    if minutes is None:
        return None
    elif minutes < 90:
        return 'Short'
    elif 90 <= minutes <= 120:
        return 'Standard'
    elif 120 < minutes <= 150:
        return '120-150 min'
    else:
        return '150+ min'

def classify_duration_filter(minutes: float, category: str = None) -> str:
    if pd.isna(minutes):
        if category == '150+ min':
            return '3–4 hrs'
        return 'Unknown'
    elif minutes < 120:
        return '< 2 hrs'
    elif 120 <= minutes <= 180:
        return '2–3 hrs'
    else:
        return '3–4 hrs'

def parse_voting_count(vote_str) -> float:
    if pd.isna(vote_str):
        return np.nan
    vote_str = str(vote_str).strip().upper()
    try:
        if 'K' in vote_str:
            return int(float(vote_str.replace('K', '')) * 1_000)
        elif 'M' in vote_str:
            return int(float(vote_str.replace('M', '')) * 1_000_000)
        else:
            return int(float(vote_str.replace(',', '')))
    except Exception as e:
        logging.warning(f'Could not parse voting count "{vote_str}": {e}')
        return np.nan

# Cleaner Function
def clean_movie_data(
    input_path='data/csv/cleaned_movies.csv',
    output_path='data/csv/cleaned_movies.csv'
) -> None:
    if not os.path.exists(input_path):
        logging.error(f'File not found: {input_path}')
        return

    logging.info(f'Loading data from: {input_path}')
    df = pd.read_csv(input_path)

    # Convert duration
    logging.info('Converting "Duration_Total" to minutes...')
    df['Duration_Minutes'] = df['Duration_Total'].apply(convert_duration_to_minutes)

    # Add two duration categories
    logging.info('Categorizing durations for display...')
    df['Duration_Category'] = df['Duration_Minutes'].apply(categorize_duration)

    logging.info('Classifying durations for filtering...')
    df['Duration'] = df.apply(
        lambda row: classify_duration_filter(row['Duration_Minutes'], row.get('Duration_Category')),
        axis=1
    )

    # Parse voting counts
    logging.info('Parsing "Voting_Counts"...')
    df['Voting_Counts'] = df['Voting_Counts'].apply(parse_voting_count)

    # Save cleaned CSV
    df.to_csv(output_path, index=False)
    logging.info(f'Cleaned CSV saved to: {output_path}')

# Script Entry Point
if __name__ == '__main__':
    clean_movie_data()