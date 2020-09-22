from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

game_words = {
    "p2w": -0.5,
    "pay-to-win": -0.5,
    "sjw": -0.8,
    "garbage": -1,
    "linear": -0.1,
    "ZERO": -0.5,
    "bug": -0.6,
    "crash": -0.8,
    "patch": 0.2,
    "skills": 0.2,
    "fun": 0.6,
    "funny": 0.6,
    "catchy": 0.4,
    "boring": -0.6,
    "balance": 0.7,
    "unbalance": -0.7,
    "microtransaction": -0.2,
    "lag": -0.3,
    "mod": 0.4,
    "toxic": -0.9,
    "trolls": -0.4,
    "hacker": -0.5,
    "camper": -0.2,
    "aimbot": -0.1,
    "drop": -0.5
}

analyzer.lexicon.update(game_words)

def filter_review_eng(language, review):
    if language == 'en':
        return get_sentiment(review)
    return "NIE" #Not in English

def get_sentiment(phrase):
    if phrase.strip() is "":
        return "NC"
    polarity = analyzer.polarity_scores(phrase)         
    if polarity["compound"] >= 0.05:
        return 'positive'
    elif polarity["compound"] <= -0.05:
        return 'negative'
    else:
        return 'mixed'

def get_validy(sentiment, rating, review):
    if sentiment == 'NIE':
        return 'NIE'
    elif (review.strip == "") or (sentiment == 'positive' and rating < 3) or (sentiment == 'negative' and rating > 7):
        return 'troll'
    else:
        return 'normal'
    