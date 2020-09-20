import datetime
from langdetect import detect
import sentiment as sent

def get_review(_review):
    language = get_language(_review)
    sentim = sent.filter_review_eng(language, _review['review'])
    return {
            'name': _review['name'],
            'platform': _review['platform'],
            'rating': _review['rating'],
            'date': get_date(_review),
            'language': language,
            'sentiment': sentim,
            'validy': sent.get_validy(sentim, _review['rating']),
            'review': clean_review(_review)
            }

def clean_review(review):
    return review['review'].replace('\r',' ')

def get_date(review):
    date = review['date']
    return datetime.datetime.strptime(date, '%b %d, %Y').date()

def get_language(review):
    text = review['review']
    return detect(text)