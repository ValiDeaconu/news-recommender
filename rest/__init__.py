from flask import Blueprint, jsonify, request, session

from model import UserKeyword

from hashlib import sha256
from string import punctuation

#python -m spacy download en_core_web_sm
import spacy 

nlp = spacy.load("en_core_web_sm")

POS_TAGS = ['PROPN', 'NOUN']

ubp = Blueprint('user', __name__)
kbp = Blueprint('keyword', __name__)

Blueprints = [
    ('/user', ubp),
    ('/user_keyword', kbp)
]

def extract_keywords(text: str) -> list[str]:
    doc = nlp(text)

    # Look for composed nouns (e.g. names: "Borris Johnson")
    composed_nouns = []
    for chunk in doc.noun_chunks:
        tokens = [t.text.strip() for t in chunk if t.pos_ in POS_TAGS]
        
        if len(tokens) > 0:
            composed_nouns.append(" ".join(tokens))

    # Look for singular nouns
    singular_nouns = [
        t.text.strip() for t in doc 
        if t.text not in nlp.Defaults.stop_words 
            and t.text not in punctuation 
            and t.pos_ in POS_TAGS
            and t.text not in composed_nouns
    ]

    return composed_nouns + singular_nouns


def process_like_action(user_id: str, news: str, is_liked: bool):
    keywords = extract_keywords(news)

    user_keywords = UserKeyword.find_all_by_user_id(user_id = user_id)
    user_keywords_dict = {}
    for k in user_keywords:
        user_keywords_dict[k.keyword] = k

    for k in keywords:
        if k in user_keywords_dict:
            if is_liked != user_keywords_dict[k].liked:
                user_keywords_dict[k].delete()
        else:
            UserKeyword(user_id = user_id, keyword = k, liked = is_liked).save()


# Add keywords based on disliked news
@kbp.route('/dislike-news', methods=["POST"])
def dislike_news():
    user_id = session.get('user_id')
    news = request.json['news']

    process_like_action(user_id, news, is_liked=False)
  
    return ""


# Add keywords based on liked news
@kbp.route('/like-news', methods=["POST"])
def like_news():
    user_id = session.get('user_id')
    news = request.json['news']

    process_like_action(user_id, news, is_liked=True)

    return ""