# IMDb 2024 Movie Dashboard
This project is an end-to-end movie analysis pipeline using IMDb data scraped in 2024. It includes data scraping, cleaning, transformation, exploratory data analysis (EDA), SQL integration, and a fully interactive Streamlit dashboard.

---

## Project Structure

```
imdb_2024_scraper_dashboard/
│
├── data/
│   └── csv/                                # CSV files
│       ├── action_movies.csv
│       ├── comedy_movies.csv
│       ├── drama_movies.csv
│       ├── horror_movies.csv
│       ├── romance_movies.csv
│       ├── cleaned_movies.csv
│       └── eda_cleaned.csv
│
├── notebooks/
│   └── imdb_eda.ipynb                      # Exploratory Data Analysis (EDA)
│
├── scripts/
│   ├── imdb_scraper.py                     # Scrapes IMDb movies by genre
│   ├── merge_csv_files.py                  # Merges all CSVs
│   ├── movie_data_cleaner.py               # Cleans and transforms data
│   └── database/
│       ├── load_and_test_mysql.py          # Checks database connection and Loads data to MySQL
│       └── sql/
│           └── all_queries.sql             # MySQL queries used in project
│
├── screenshots/                            # Contains visual proof of dashboard and UI functionality
│   ├── screenshot1_streamlit_dashbord.png
│   ├── screenshot2_streamlit_dashbord.png
│   ├── screenshot3_streamlit_dashbord.png
│   ├── screenshot4_streamlit_dashbord.png
│   └── screenshot5_streamlit_dashbord.png
│
├── app.py                                  # Streamlit dashboard app
├── project_report.pdf                      # Final project report
├── requirements.txt                        # Project dependencies
└── README.md                               # This documentation file
```

---

## Project Goals

Scrape IMDb data for various genres (action, comedy, drama, horror, romance).

Clean, merge, and transform raw movie data.

Conduct exploratory data analysis on ratings, votes, and durations.

Save cleaned datasets in CSV and MySQL formats.

Build a dynamic and interactive dashboard using Streamlit.

---

## Key Features

- **IMDb Scraper**:
  - Scrapes movie metadata for selected genres using `requests`, `selenium` and `BeautifulSoup`

- **Data Cleaning**:
  - Handles missing values
  - Formats ratings, votes, durations
  - Classifies movies by duration categories

- **Exploratory Data Analysis**:
  - Histogram of ratings
  - Bar plots for genres
  - Correlation matrix
  - Genre-based rating trends
  - Scatter and box plots for voting/rating analysis

- **Streamlit Dashboard**:
  - Filters: Genre, Rating, Votes, Duration
  - Top 10 movies by rating
  - Genre distribution charts
  - Voting and rating insights
  - Duration-based patterns
  - Real-time dynamic updates

- **MySQL Integration**:
  - Cleaned dataset is loaded into MySQL
  - SQL scripts and queries provided for advanced analysis

---

## Technologies Used

- **Programming**: Python
- **Libraries**: `pandas`, `numpy`, `matplotlib`, `seaborn`, `requests`,`selenium`, `beautifulsoup4`
- **Dashboard**: Streamlit
- **Database**: MySQL, `mysql-connector-python`
- **Development**: Jupyter Notebook, Markdown

---

## How to Run the Project

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/imdb_2024_scraper_dashboard.git
cd imdb_2024_scraper_dashboard
```
---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
---

### 3. Scrape IMDb Data (Multiple Genres)

Run the scraper script **multiple times**, changing the genre name inside the script each time (`'action'`, `'romance'`, `'comedy'`, etc.):

```bash
python scripts/imdb_scraper.py
```

Repeat this for all genres you want. This will create multiple CSV files (e.g., `action_movies.csv`, `romance_movies.csv`, etc.).

---

### 4. Merge CSV Files

Once all genre CSVs are created, merge them:

```bash
python scripts/merge_csv_files.py
```

This generates `cleaned_movies.csv`.

---

### 5. Clean the Movie Dataset

Run the cleaning script:

```bash
python scripts/movie_data_cleaner.py
```

This script:
- Cleans and transforms the dataset
- Outputs an updated `cleaned_movies.csv`

---
### 6. Perform Exploratory Data Analysis (EDA)

Launch Jupyter Notebook:

```bash
jupyter notebook notebooks/imdb_eda.ipynb
```

Steps inside notebook:
- Explore visualizations and patterns
- Conduct summary statistics
- Save the final dataset as:

This generates `eda_cleaned.csv`.

---
### 7. Load Data to MySQL

Run the unified script:

```bash
python scripts/database/load_and_test_mysql.py
```

This script performs two key operations:

#### 1. Test MySQL Connection
- Verifies that your MySQL server is running
- Uses the provided credentials (host, user, password, database) to ensure access
- Displays a success message if the connection is valid
- Aborts if the connection fails

#### 2. Load Cleaned Data to MySQL
- Reads the `eda_cleaned.csv` file from `data/csv/`
- Creates a table named `movies_2024` if it doesn't already exist
- Inserts each row of movie data into the MySQL table
- Commits all changes to your `imdb_movies` database.

---
### 8. (Optional) Run SQL Queries for Analysis

Open MySQL Workbench or any client and execute:

```sql
-- Located in:
scripts/database/sql/imdb.sql
```

Analyze movies via SQL based on ratings, votes, genres, etc.

---
### 9. Launch the Streamlit Dashboard

```bash
streamlit run app.py
```

Explore the visual interface and apply filters interactively.

---

## Screenshots

The `screenshots/` folder contains visual samples of the working dashboard and plots from the project, demonstrating its interactivity and UI functionality.

---

## Deliverables

- Genre-wise and cleaned movie datasets (CSV)
- SQL-ready MySQL database of movies
- Full EDA notebook with plots and summaries
- Interactive Streamlit dashboard
- Project report PDF
- Documentation and deployment-ready code

---

## Author

**Dinesh Kumar**  
LinkedIn: [https://www.linkedin.com/in/dineshkumar-dhanapal-9ab038327/](https://www.linkedin.com/in/dineshkumar-dhanapal-9ab038327/)

---

## License

This project is created for academic and personal learning purposes. Contributions or forks are welcome with credit.