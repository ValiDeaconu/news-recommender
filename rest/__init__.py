from flask import Blueprint, send_file, jsonify, request, session, make_response
from os.path import join
from passlib.hash import sha256_crypt

from model import User, UserCategory, UserKeyword

from form.register import Form as RegisterForm
from form.login import Form as LoginForm

import requests

from hashlib import sha256
from string import punctuation

#python -m spacy download en_core_web_sm
import spacy 

ubp = Blueprint('user', __name__)
kbp = Blueprint('keyword', __name__)

Blueprints = [
    ('/user', ubp),
    ('/user_keyword', kbp)
]


# Get headlines by category
@ubp.route('/get-headlines', methods=["GET"])
def get_headlines():
    url = ('https://newsapi.org/v2/top-headlines?country=ro&category=')
    for category in UserCategory.find_all_by_user_id(session.get("user").id) :
        url = url + ' OR ' + category

    url = url + ('&apiKey=a29ea4304a564e7bbf8275c596a64dd1')

    response = requests.get(url)

    return response.json(), 200

# Add keywords based on disliked news
@kbp.route('/dislike-news', methods=["POST"])
def dislike_news():
    user_id = session.get('user').id
    news = request.json['news']

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(news)

    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    pos_tag = ['PROPN', 'NOUN']

    keywords = []
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            keywords.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            keywords.append(token.text)

    for keyword in keywords:
        UserKeyword(user_id = user_id, keyword = keyword, liked = False).save()

    return jsonify([{'keywords': list(set(keywords))}])


# Add keywords based on liked news
@kbp.route('/like-news', methods=["POST"])
def like_news():
    user_id = session.get('user_id')
    news = request.json['news']

    nlp = spacy.load("en_core_web_sm")

    doc = nlp(news)

    print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
    print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

    pos_tag = ['PROPN', 'NOUN']

    keywords = []
    for chunk in doc.noun_chunks:
        final_chunk = ""
        for token in chunk:
            if (token.pos_ in pos_tag):
                final_chunk =  final_chunk + token.text + " "
        if final_chunk:
            keywords.append(final_chunk.strip())


    for token in doc:
        if (token.text in nlp.Defaults.stop_words or token.text in punctuation):
            continue
        if (token.pos_ in pos_tag):
            keywords.append(token.text)

    for keyword in keywords:
        UserKeyword(user_id = user_id, keyword = keyword, liked = True).save()

    return jsonify([{'keywords': list(set(keywords))}])