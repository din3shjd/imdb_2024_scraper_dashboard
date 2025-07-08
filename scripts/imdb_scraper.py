""" 
imdb_scraper.py
Scrapes IMDb movie data for a given genre and year using Selenium and BeautifulSoup.
Saves the scraped data to: data/csv/{genre}_movies.csv """
import os
import re
import time
import logging
import pandas as pd
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Logging Configuration
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Setup Chrome Driver
def setup_driver(headless: bool = False) -> uc.Chrome:
    options = uc.ChromeOptions()
    options.headless = headless
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0')
    return uc.Chrome(options=options)

# Parse Single Movie Card
def parse_movie_card(movie, genre: str) -> Dict[str, str]:
    try:
        title_tag = movie.find('h3')
        name = re.sub(r'^\d+\.\s*', '', title_tag.get_text(strip=True)) if title_tag else 'N/A'

        rating_tag = movie.find('span', string=re.compile(r'\d+\.\d+'))
        rating = rating_tag.get_text(strip=True) if rating_tag else 'N/A'

        votes_tag = movie.find('span', class_='ipc-rating-star--voteCount')
        votes = ''.join(votes_tag.stripped_strings).strip('()') if votes_tag else 'N/A'

        duration_tag = movie.find('span', string=re.compile(r'\d+h\s*\d+m'))
        duration = duration_tag.get_text(strip=True) if duration_tag else 'N/A'

        return {
            'Movie_Name': name,
            'Rating': rating,
            'Voting_Counts': votes,
            'Duration_Total': duration,
            'Genre': genre.capitalize()
        }

    except Exception as e:
        logging.warning(f'Error parsing movie: {e}')
        return {}

# Scrape Movies by Genre
def scrape_genre_movies(genre: str, year: int = 2024, max_movies: int = 250, headless: bool = False):
    logging.info(f'Starting IMDb scraping for genre: {genre}, year: {year}')

    driver = setup_driver(headless)
    wait = WebDriverWait(driver, 15)
    os.makedirs('data/csv', exist_ok=True)

    url = (
        f'https://www.imdb.com/search/title/?title_type=feature'
        f'&release_date={year}-01-01,{year}-12-31&genres={genre}'
    )
    driver.get(url)

    collected_movies: List[Dict[str, str]] = []

    while len(collected_movies) < max_movies:
        time.sleep(2)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        movie_cards = soup.find_all('li', class_='ipc-metadata-list-summary-item')

        logging.info(f'Movies loaded on page: {len(movie_cards)}')

        for card in movie_cards[len(collected_movies):]:
            data = parse_movie_card(card, genre)
            if data:
                collected_movies.append(data)
            if len(collected_movies) >= max_movies:
                break

        if len(collected_movies) >= max_movies:
            break

        try:
            load_more = wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//span[contains(text(), "50 more")]/ancestor::button')))
            driver.execute_script('arguments[0].click();', load_more)
            logging.info('Clicked "50 more" to load more movies.')
        except:
            logging.info('No more results or "50 more" button not found.')
            break

    driver.quit()

    df = pd.DataFrame(collected_movies).drop_duplicates()
    output_path = os.path.join('data', 'csv', f'{genre.lower()}_movies.csv')
    df.to_csv(output_path, index=False)

    logging.info(f'Saved {len(df)} unique movies to {output_path}')

# Entry Point
if __name__ == '__main__':
    scrape_genre_movies(genre='action', max_movies=250, headless=False)
