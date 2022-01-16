from model import User, UserKeyword, UserCategory

from flask import logging
from requests import get as fetch
from random import sample, shuffle
from urllib.parse import quote_plus as urlencode


PAGE_SIZE = 50
NEWS_API_KEY = 'a29ea4304a564e7bbf8275c596a64dd1'
NEWS_API_EVERYTHING_ENDPOINT = f'https://newsapi.org/v2/everything?apiKey={NEWS_API_KEY}&sortBy=publishedAt&pageSize={PAGE_SIZE}'
NEWS_API_HEADLINES_ENDPOINT = f'https://newsapi.org/v2/top-headlines?apiKey={NEWS_API_KEY}&sortBy=publishedAt&country=us&pageSize={PAGE_SIZE}'

def _fetch(url: str):
    print(f'[INFO] Fetching from {url}')
    return fetch(url)

def get_news_for_user(user_id: int):
    user = User.find_by_id(id=user_id)

    required_headlines = int(user.mutation_rate * PAGE_SIZE)
    required_articles = int(PAGE_SIZE - required_headlines)

    keywords = UserKeyword.find_random_sample_for_user(user_id=user_id)

    news = []

    if len(keywords) > 0:
        positive_keywords = ' OR '.join([k[0] for k in keywords if k[1]])
        negative_keywords = ' OR '.join([k[0] for k in keywords if not k[1]])
        query = urlencode(f'({positive_keywords}) AND NOT ({negative_keywords})')
        print(f"DEBUG: Searching with query={query}")
        url = f'{NEWS_API_EVERYTHING_ENDPOINT}&q={query}'
        response = _fetch(url).json()
        everything_articles = response['articles']

        if len(everything_articles) >= required_articles:
            news = sample(everything_articles, required_articles)
        else:
            headline_surplus = required_articles - len(everything_articles)
            required_headlines += headline_surplus
    else:
        required_headlines = PAGE_SIZE

    user_categories = UserCategory.find_all_by_user_id(user_id=user_id)
    shuffle(user_categories)

    categories = [c.category for c in user_categories]

    for category in categories:
        url = f'{NEWS_API_HEADLINES_ENDPOINT}&category={category}'
        response = _fetch(url).json()
        headlines_articles = response['articles']
        l = len(headlines_articles)

        if l == required_headlines:
            news.extend(headlines_articles)
            break
        
        if l > required_headlines:
            sampled_articles = sample(headlines_articles, required_headlines)
            news.extend(sampled_articles)
            break

        if l < required_headlines:
            news.extend(headlines_articles)
    
    return news
           
