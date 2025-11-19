from datetime import datetime
import csv
import os

from dotenv import load_dotenv
import requests

load_dotenv()


def get_top_headlines(category: str):
    API_KEY = os.getenv("NEWS_API_KEY")
    BASE_URL = "https://newsapi.org/v2/top-headlines"

    params = {"category": category, "apiKey": API_KEY, "pageSize": 5}

    response = requests.get(BASE_URL, params=params, timeout=10)

    if response.status_code == 200:
        data = response.json()
        articles = data["articles"]
        headlines = [
            {
                "category": category,
                "publishedAt": article["publishedAt"],
                "title": article["title"].strip(),
                "source": article["source"]["name"].strip(),
                "url": article["url"],
            }
            for article in articles[:5]
        ]
        return headlines
    else:
        print(f"Error: {response.status_code}")
        return []


def merge_headlines(*lists):
    merged_list = []
    for lst in lists:
        merged_list.extend(lst)
    return merged_list


def save_headlines_to_csv(headlines, filename):
    keys = headlines[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(headlines)


general_headlines = get_top_headlines("general")
business_headlines = get_top_headlines("business")
science_headlines = get_top_headlines("science")
tech_headlines = get_top_headlines("technology")

merged_headlines = merge_headlines(
    general_headlines, business_headlines, science_headlines, tech_headlines
)

today_datetime = datetime.today().strftime("%Y-%m-%d_%H%M")
save_headlines_to_csv(merged_headlines, f"headlines/{today_datetime}.csv")
