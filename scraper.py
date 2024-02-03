# python
import random
import requests
import os

# third party
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# URLs to scrape
urls = {
    "Towards Data Science": "https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}",
    "UX Collective": "https://uxdesign.cc/archive/{0}/{1:02d}/{2:02d}",
    "The Startup": "https://medium.com/swlh/archive/{0}/{1:02d}/{2:02d}",
    "The Writing Cooperative": "https://writingcooperative.com/archive/{0}/{1:02d}/{2:02d}",
    "Data Driven Investor": "https://medium.com/datadriveninvestor/archive/{0}/{1:02d}/{2:02d}",
    "Better Humans": "https://medium.com/better-humans/archive/{0}/{1:02d}/{2:02d}",
    "Better Marketing": "https://medium.com/better-marketing/archive/{0}/{1:02d}/{2:02d}",
}


def is_leap(year):
    """
    Determine if a given year is a leap year.

    A leap year is defined as a year that is divisible by 4,
    except for years which are both divisible by 100 and not divisible by 400.
    For example, 2000 and 2004 are leap years, but 1900 is not.

    Args:
    year (int): The year to check.

    Returns:
    bool: True if the year is a leap year, False otherwise.
    """
    # The year is a leap year if it is divisible by 4
    # AND (it is not divisible by 100 OR it is divisible by 400).
    # This condition checks all those rules and returns True if they are all met,
    # meaning the year is a leap year; otherwise, it returns False.
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def convert_day(day, year):
    """
    Convert a day of the year into its corresponding month and day.

    This function takes a day number (1 through 365 or 366 for leap years) and a year,
    and calculates which month and day of the month this number corresponds to.

    Args:
    day (int): The day of the year (1 through 365 or 366).
    year (int): The year, used to account for leap years.

    Returns:
    tuple: A tuple containing two integers, where the first integer is the month (1 through 12)
           and the second integer is the day of the month.

    The function accounts for leap years by checking if the year is a leap year
    using the `is_leap` function. If it is a leap year, February has 29 days; otherwise, it has 28.
    """
    # List of days in each month. February's days depend on whether the year is a leap year.
    month_days = [
        31,
        29 if is_leap(year) else 28,  # February: 29 days if leap year, otherwise 28
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31,
    ]
    m = 0  # Index for the month in the month_days list, starting with January (index 0)
    d = 0  # Day of the month

    # Iterate through each month, subtracting the number of days in that month from 'day'
    # until 'day' is no longer greater than the number of days in the month.
    # This loop determines the month and the exact day of the month.
    while day > 0:
        d = day  # Store the current value of 'day' as the day of the month
        day -= month_days[
            m
        ]  # Subtract the number of days in the current month from 'day'
        m += 1  # Move to the next month

    # Return the month (plus one because months are 1-indexed) and the day of the month.
    # The loop decrements 'day' until it is no longer positive, which means the last subtraction
    # might make 'day' go below 1, hence using 'd' to remember the day of the month before the last subtraction.
    return (m, d)


def get_claps(claps_str):
    """
    Convert a string representation of claps (likes or upvotes) into an integer.

    This function is designed to handle the claps count as it might appear on social media or
    articles, where large numbers are sometimes abbreviated with a 'K' to represent thousands.
    For example, '2.5K' claps would be converted to 2500.

    Args:
    claps_str (str): The string representing the number of claps, which may include
                     a 'K' to denote thousands.

    Returns:
    int: The number of claps as an integer. If the input is None, an empty string,
         or cannot be converted to an integer, returns 0.
    """
    # Check if the input string is None or empty. If so, return 0.
    if claps_str is None or claps_str == "":
        return 0

    # Replace 'K' in the string with '000' to convert thousands to a full number.
    # This is necessary for strings like '2.5K', which should be converted to 2500.
    claps_str = claps_str.replace("K", "000")

    # Attempt to convert the modified string to a float first (to handle decimal points)
    # and then to an integer. This conversion handles strings like '2.5K' correctly.
    try:
        return int(float(claps_str))
    except ValueError:
        # If conversion fails (e.g., due to an invalid format in the string),
        # catch the ValueError and return 0.
        return 0


# Set the target year for scraping.
year = 2023
# Randomly select 50 days from the year, accounting for leap years.
selected_days = random.sample(range(1, 367 if is_leap(year) else 366), 50)

# Initialize an empty list to store data collected from each article.
data = []
# Initialize an article ID counter to uniquely identify each article.
article_id = 0

# Iterate over each selected day, displaying progress with tqdm.
for d in tqdm(selected_days, desc="Processing days"):
    # Convert the day of the year to a month and day.
    month, day = convert_day(d, year)
    # Iterate over each publication URL in the urls dictionary.
    for publication, url in urls.items():
        # Format the URL with the current year, month, and day.
        formatted_url = url.format(year, month, day)
        # Make an HTTP request to the formatted URL.
        response = requests.get(formatted_url)
        # Proceed if the HTTP request was successful (status code 200).
        if response.status_code == 200:
            # Parse the HTML content of the page using BeautifulSoup.
            soup = BeautifulSoup(response.content, "html.parser")
            # Find all article containers using the specified class.
            articles = soup.find_all(
                "div",
                class_="cardChromeless u-marginTop20 u-paddingTop10 u-paddingBottom15 u-paddingLeft20 u-paddingRight20",
            )
            # Iterate over each article container found.
            for article in articles:
                # Attempt to find the article title using the specified class.
                title_tag = article.find(
                    "h3", class_="graf graf--h3 graf-after--figure graf--title"
                )
                # Extract the text of the title tag if found, otherwise use a placeholder.
                title = title_tag.text if title_tag else "No Title Found"
                # Attempt to find the claps count using the specified class.
                claps_div = article.find(
                    "div", class_="multirecommend js-actionMultirecommend u-flexCenter"
                )
                # Convert the text of the claps count to an integer, or use 0 if not found.
                claps = get_claps(claps_div.text) if claps_div else 0
                # Increment the article ID for the next article.
                article_id += 1
                # Append the collected data for this article to the data list.
                data.append(
                    {
                        "id": article_id,
                        "publication": publication,
                        "date": f"{year}-{month:02d}-{2:02d}",
                        "title": title,
                        "claps": claps,
                    }
                )

# Convert the list of data into a pandas DataFrame.
df = pd.DataFrame(data)

# Ensure the 'data' directory exists
if not os.path.exists('data'):
    os.makedirs('data')

# Save the DataFrame to a CSV file for later use or analysis.
df.to_csv("data/medium_data.csv", index=False)

# Print the total number of articles scraped to the console.
print(f"Scraped {len(data)} articles.")
