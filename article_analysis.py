import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import re


# Function to clean text and split into words
def clean_and_split(text):
    words = re.sub(r"\W+", " ", text.lower()).split()
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
    return [word for word in words if word not in stopwords]


# Analyze keywords and publication popularity
def analyze_medium_data(df):
    most_popular_articles = df.sort_values(by="claps", ascending=False).head(10)
    keywords = Counter()
    for title in most_popular_articles["title"]:
        keywords.update(clean_and_split(title))
    print("Most common keywords in titles of the most popular articles:")
    for word, count in keywords.most_common(10):
        print(f"{word}: {count}")

    publication_popularity = (
        df.groupby("publication")["claps"].mean().sort_values(ascending=False)
    )
    print("\nAverage claps by publication:")
    print(publication_popularity)


# Load the dataset
df = pd.read_csv("data/medium_data.csv")

# Convert 'date' to datetime and extract 'month' and 'year'
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Initial analysis
analyze_medium_data(df)

# Seasonal analysis for patterns in specific times of the year
monthly_claps = df.groupby("month")["claps"].mean()
# Assuming monthly_claps is already calculated
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=monthly_claps.index, y=monthly_claps.values, palette="coolwarm")
plt.title("Average Claps by Month")
plt.xlabel("Month")
plt.ylabel("Average Claps")
plt.xticks(
    ticks=range(0, 12),
    labels=[
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ],
)

# Annotate each bar with the exact value
for p in ax.patches:
    ax.annotate(
        format(p.get_height(), ".2f"),
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 10),
        textcoords="offset points",
    )

plt.show()
