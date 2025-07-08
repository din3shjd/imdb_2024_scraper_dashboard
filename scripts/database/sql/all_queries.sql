-- IMDb 2024 SQL Project: Clean & Analyze Movie Data

-- Step 1: Use IMDb Database
USE imdb_movies;

-- Step 2: Create Cleaned Table
DROP TABLE IF EXISTS cleaned_movies;
CREATE TABLE cleaned_movies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Movie_Name VARCHAR(255),
    Rating FLOAT,
    Voting_Counts INT,
    Genre VARCHAR(255),
    Duration VARCHAR(50)
);

-- Step 3: Preview Table
SELECT COUNT(*) AS total_rows FROM cleaned_movies;
SELECT * FROM cleaned_movies LIMIT 10;

-- Step 4: Allow Non-Key Updates
SET SQL_SAFE_UPDATES = 0;

-- Step 5: Clean Movie_Name
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, CHAR(160), '');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, UNHEX('E2808B'), '');

-- Step 6: Replace Accented Characters
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'à', 'a');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'á', 'a');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'é', 'e');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'è', 'e');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ê', 'e');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'í', 'i');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ó', 'o');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ö', 'o');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ú', 'u');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ñ', 'n');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'Ñ', 'N');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ü', 'u');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ç', 'c');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'ø', 'o');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'Á', 'A');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'É', 'E');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'Í', 'I');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'Ó', 'O');
UPDATE cleaned_movies SET Movie_Name = REPLACE(Movie_Name, 'Ú', 'U');

-- Step 7: Handle NULLs
UPDATE cleaned_movies SET Voting_Counts = 0 WHERE Voting_Counts IS NULL;
UPDATE cleaned_movies SET Duration = 'Unknown' WHERE Duration IS NULL;
DELETE FROM cleaned_movies
WHERE Movie_Name IS NULL AND Rating IS NULL AND Voting_Counts IS NULL
  AND Genre IS NULL AND Duration IS NULL;

-- Step 8: Aggregations
SELECT Genre, COUNT(*) AS Movie_Count FROM cleaned_movies GROUP BY Genre ORDER BY Movie_Count DESC;
SELECT Genre, ROUND(AVG(Rating), 2) AS Avg_Rating FROM cleaned_movies GROUP BY Genre ORDER BY Avg_Rating DESC;
SELECT Genre, MAX(Rating) AS Max_Rating FROM cleaned_movies GROUP BY Genre;
SELECT Genre, MIN(Rating) AS Min_Rating FROM cleaned_movies GROUP BY Genre;
SELECT Duration, COUNT(*) AS Movie_Count FROM cleaned_movies GROUP BY Duration ORDER BY Movie_Count DESC;
SELECT Duration, ROUND(AVG(Rating), 2) AS Avg_Rating FROM cleaned_movies GROUP BY Duration ORDER BY Avg_Rating DESC;
SELECT Genre, Duration, COUNT(*) AS Count FROM cleaned_movies GROUP BY Genre, Duration ORDER BY Genre, Count DESC;

-- Step 9: Top Movies
SELECT Movie_Name, Genre, Rating, Voting_Counts FROM cleaned_movies ORDER BY Rating DESC, Voting_Counts DESC LIMIT 10;
SELECT Movie_Name, Genre, Rating, Voting_Counts FROM cleaned_movies ORDER BY Voting_Counts DESC LIMIT 10;
SELECT Movie_Name, Rating FROM cleaned_movies WHERE Rating = (SELECT MAX(Rating) FROM cleaned_movies) LIMIT 1;
SELECT Movie_Name, Voting_Counts FROM cleaned_movies ORDER BY Voting_Counts DESC LIMIT 1;

-- Step 10: Indexes
CREATE INDEX idx_genre ON cleaned_movies (Genre);
CREATE INDEX idx_rating ON cleaned_movies (Rating);
CREATE INDEX idx_voting_counts ON cleaned_movies (Voting_Counts);

-- Step 11: Views
CREATE OR REPLACE VIEW view_avg_rating_by_genre AS
SELECT Genre, ROUND(AVG(Rating), 2) AS Avg_Rating FROM cleaned_movies GROUP BY Genre;

CREATE OR REPLACE VIEW view_genre_duration_breakdown AS
SELECT Genre, Duration, COUNT(*) AS Movie_Count FROM cleaned_movies GROUP BY Genre, Duration;

CREATE OR REPLACE VIEW view_top10_by_rating AS
SELECT Movie_Name, Genre, Rating, Voting_Counts FROM cleaned_movies ORDER BY Rating DESC, Voting_Counts DESC LIMIT 10;

CREATE OR REPLACE VIEW view_top10_by_votes AS
SELECT Movie_Name, Genre, Rating, Voting_Counts FROM cleaned_movies ORDER BY Voting_Counts DESC LIMIT 10;
