"""
app.py
IMDb 2024 Movie Dashboard - Streamlit App
Visualizes and filters IMDb movie data.
Dataset: data/csv/eda_cleaned.csv   """
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mysql.connector

# Load Data from MySQL
def fetch_movies_from_mysql():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Leo@root',
            database='imdb_movies'
        )
        query = 'SELECT * FROM cleaned_movies'
        df = pd.read_sql(query, connection)
        return df
    except mysql.connector.Error as e:
        st.error(f'Database connection error: {e}')
        return pd.DataFrame()
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

df = fetch_movies_from_mysql()

# Page Config & Title
st.set_page_config(page_title='IMDb 2024 Movie Dashboard', layout='wide')
st.title('IMDb 2024 Movie Dashboard')

# Sidebar Filters
st.sidebar.header('Filter Movies')

selected_genres = st.sidebar.multiselect(
    'Select Genres', sorted(df['Genre'].dropna().unique())
)

selected_durations = st.sidebar.multiselect(
    'Select Duration', sorted(df['Duration'].dropna().unique())
)

rating_range = st.sidebar.slider(
    'Minimum Rating',
    float(df['Rating'].dropna().min()),
    float(df['Rating'].dropna().max()),
    float(df['Rating'].dropna().min())
)

if df['Voting_Counts'].dropna().empty:
    min_votes = 0
    max_votes = 1000  # default dummy max
else:
    min_votes = int(df['Voting_Counts'].dropna().min())
    max_votes = int(df['Voting_Counts'].dropna().max())
    if min_votes == max_votes:
        max_votes += 100  # ensure a usable slider

votes_range = st.sidebar.slider(
    'Minimum Voting Counts',
    min_votes,
    max_votes,
    min_votes
)


# Apply Filters
filtered_df = df.copy()

if selected_genres:
    filtered_df = filtered_df[filtered_df['Genre'].isin(selected_genres)]

if selected_durations:
    filtered_df = filtered_df[filtered_df['Duration'].isin(selected_durations)]

filtered_df = filtered_df[
    (filtered_df['Rating'] >= rating_range) &
    (filtered_df['Voting_Counts'] >= votes_range)
]

columns_to_display = ['Movie_Name', 'Genre', 'Rating', 'Voting_Counts', 'Duration']

# Utility Functions
def format_table(df):
    df = df.copy()
    df['Rating'] = df['Rating'].apply(lambda x: str(round(x, 1)))
    df['Voting_Counts'] = df['Voting_Counts'].apply(lambda x: f'{int(x):,}')
    return df

def uniform_style(df):
    return df.style.set_properties(**{
        'text-align': 'left',
        'font-family': 'monospace',
        'font-size': '14px',
        'padding': '6px'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('text-align', 'left')]
    }])

# Filtered Movies Table
st.markdown('---')
st.subheader('Filtered Movies')

if filtered_df.empty:
    st.warning('No data available for the selected filters.')
else:
    st.dataframe(uniform_style(format_table(filtered_df[columns_to_display])), use_container_width=True)

# Top 10 Movies by Rating
st.markdown('---')
st.subheader('Top 10 Movies by Rating')

top_rating = filtered_df.sort_values(by='Rating', ascending=False).head(10)
if not top_rating.empty:
    st.dataframe(uniform_style(format_table(top_rating[columns_to_display])), use_container_width=True)
else:
    st.info('No data to show.')

# Top 10 Movies by Voting
st.markdown('---')
st.subheader('Top 10 Movies by Voting Counts')

top_votes = filtered_df.sort_values(by='Voting_Counts', ascending=False).head(10)
if not top_votes.empty:
    st.dataframe(uniform_style(format_table(top_votes[columns_to_display])), use_container_width=True)
else:
    st.info('No data to show.')

# Top Rated Movie per Genre
st.markdown('---')
st.subheader('Top Rated Movie per Genre')

if not filtered_df.empty:
    top_per_genre = filtered_df.loc[filtered_df.groupby('Genre')['Rating'].idxmax()]
    st.dataframe(uniform_style(format_table(top_per_genre[columns_to_display])), use_container_width=True)
else:
    st.info('No data to show.')

# Highest & Lowest Rated Movies
st.markdown('---')
st.subheader('Highest Rated Movie')

if not filtered_df.empty:
    highest = filtered_df.loc[filtered_df['Rating'].idxmax()]
    st.dataframe(uniform_style(format_table(pd.DataFrame([highest])[columns_to_display])), use_container_width=True)
else:
    st.info('No data to show.')

st.subheader('Lowest Rated Movie')

if not filtered_df.empty:
    lowest = filtered_df.loc[filtered_df['Rating'].idxmin()]
    st.dataframe(uniform_style(format_table(pd.DataFrame([lowest])[columns_to_display])), use_container_width=True)
else:
    st.info('No data to show.')

# Ratings by Genre and Duration
st.markdown('---')
st.subheader('Ratings by Genre and Duration')

pivot_table = filtered_df.pivot_table(
    index='Genre',
    columns='Duration',
    values='Rating',
    aggfunc='mean'
).round(2).fillna('')

st.dataframe(uniform_style(pivot_table.astype(str)), use_container_width=True)

# Genre Distribution
st.markdown('---')
st.subheader('Genre Distribution')

genre_counts = filtered_df['Genre'].value_counts()
if not genre_counts.empty:
    fig, ax = plt.subplots()
    genre_counts.plot(kind='bar', ax=ax, color='skyblue', edgecolor='black')
    ax.set_ylabel('Count')
    ax.set_xlabel('Genre')
    st.pyplot(fig)
else:
    st.info('No data to plot.')

# Average Rating by Genre
st.markdown('---')
st.subheader('Average Rating by Genre')

avg_rating = filtered_df.groupby('Genre')['Rating'].mean().sort_values()
if not avg_rating.empty:
    fig, ax = plt.subplots()
    avg_rating.plot(kind='barh', ax=ax, color='mediumseagreen', edgecolor='black')
    ax.set_xlabel('Average Rating')
    st.pyplot(fig)
else:
    st.info('No data to plot.')

# Total Voting Counts by Genre
st.markdown('---')
st.subheader('Total Voting Counts by Genre')

votes_by_genre = filtered_df.groupby('Genre')['Voting_Counts'].sum()
if not votes_by_genre.empty:
    fig, ax = plt.subplots()
    votes_by_genre.plot(kind='bar', ax=ax, color='coral', edgecolor='black')
    ax.set_ylabel('Total Votes')
    st.pyplot(fig)
else:
    st.info('No data to plot.')

# Rating Distribution
st.markdown('---')
st.subheader('Rating Distribution')

if not filtered_df['Rating'].empty:
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['Rating'], kde=True, bins=20, ax=ax, color='purple', edgecolor='black')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)
else:
    st.info('No data to plot.')

# Rating vs Voting (Scatter Plot)
st.markdown('---')
st.subheader('Rating vs Voting Correlation')

if not filtered_df.empty:
    fig, ax = plt.subplots()
    sns.scatterplot(data=filtered_df, x='Rating', y='Voting_Counts', ax=ax, color='teal', edgecolor='black')
    ax.set_xlabel('Rating')
    ax.set_ylabel('Voting Counts')
    st.pyplot(fig)
else:
    st.info('No data for scatter plot.')

# Most Popular Genres by Voting (Pie Chart)
st.markdown('---')
st.subheader('Most Popular Genres by Total Voting')

if not votes_by_genre.empty:
    fig, ax = plt.subplots()
    votes_by_genre.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90, cmap='Set3')
    ax.set_ylabel('')
    st.pyplot(fig)
else:
    st.info('No data for pie chart.')

st.markdown('---')
