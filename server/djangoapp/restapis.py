import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv("backend_url", default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    "sentiment_analyzer_url", default="http://localhost:5050/"
)


def get_request(endpoint, **kwargs):
    request_url = backend_url + endpoint
    print(f"GET from {request_url} with params {kwargs}")

    try:
        response = requests.get(request_url, params=kwargs, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Sentiment analyzer network exception occurred: {e}")
        return None
    except Exception as err:
        print(f"Unexpected error: {err}")
        return None


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict, timeout=5)
        response.raise_for_status()
        print(f"Posted review response: {response.json()}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred during post: {e}")
        return None
