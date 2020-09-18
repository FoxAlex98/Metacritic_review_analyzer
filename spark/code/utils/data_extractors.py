import datetime
from langdetect import detect

def get_review(_review):
    return {
            'name': _review['name'],
            'rating': _review['rating'],
            'date': get_date(_review),
            'language': get_language(_review),
            'review': clean_review(_review)
            #'valid': get_valid()
            }

def clean_review(review):
    return review['review'].replace('\r',' ')

def get_date(review):
    try:
        date = review['date']
        return datetime.datetime.strptime(date, '%b %d, %Y')
    except TypeError as err:
        print("///////////////////////////")
        print(err)
        print("review " + str(review))
        return datetime.datetime.now()


def get_language(review):
    try:
        text = review['review']
        return detect(text)
    except TypeError as err:
        print("///////////////////////////")
        print(err)
        print("review " + str(review))
        return "NaN"