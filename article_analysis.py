import pandas as pd
import re
from collections import Counter


def clean_and_split(text):
    """
    Cleans the input text by converting it to lowercase, removing any non-alphanumeric
    characters (including punctuation), and splitting it into individual words. Common
    stopwords are also removed from the resulting list of words.

    Args:
    text (str): The input text to be cleaned and split.

    Returns:
    list: A list of words after cleaning the input text and removing stopwords.
    """
    # Lowercase the input text and replace non-alphanumeric characters (excluding spaces)
    # with a space, then split the text into a list of words based on whitespace.
    words = re.sub(r"\W+", " ", text.lower()).split()

    # Define a list of common stopwords to be removed from the text.
    stopwords = [
        "the",
        "in",
        "to",
        "of",
        "and",
        "a",
        "is",
        "for",
        "on",
        "with",
        "as",
        "no",
        "title",
        "found",
    ]

    # Filter out the stopwords from the list of words.
    words = [word for word in words if word not in stopwords]

    return words


def analyze_medium_data(df):
    """
    Analyzes Medium articles dataset to identify patterns and insights.

    - Extracts and analyzes the most common keywords in the titles of the most popular articles.
    - Placeholder for future analysis to examine the correlation between publication dates and article popularity.
    - Aggregates data by publication to identify which ones feature the most popular articles based on average claps.

    Args:
    df (pd.DataFrame): DataFrame containing Medium articles data.
    """
    # Extract the most popular articles based on claps for keyword analysis
    most_popular_articles = df.sort_values(by="claps", ascending=False).head(10)

    # Extract and analyze keywords in titles
    keywords = Counter()
    for title in most_popular_articles["title"]:
        keywords.update(clean_and_split(title))

    print("Most common keywords in titles of the most popular articles:")
    for word, count in keywords.most_common(10):
        print(f"{word}: {count}")

    # Aggregate data by publication to see which ones feature more popular articles
    publication_popularity = (
        df.groupby("publication")["claps"].mean().sort_values(ascending=False)
    )
    print("\nAverage claps by publication:")
    print(publication_popularity)


# Main script execution
if __name__ == "__main__":
    # Load the dataset
    df = pd.read_csv("data/medium_data.csv")

    # Call the analysis function
    analyze_medium_data(df)
