from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()

def filter_review_eng(language, review):
    if language == 'en':
        return get_sentiment(review)
    return "NIE"

def get_sentiment(phrase):
    polarity = analyzer.polarity_scores(phrase)         
    if polarity["compound"] >= 0.05:
        if polarity['neg'] > 0.05:
            return 'ironic'
        return 'positive'
    elif polarity["compound"] <= -0.05:
        if polarity['pos'] > 0.05:
            return 'ironic'
        return 'negative'
    else:
        if polarity["pos"] > 0 and polarity["neg"] > 0:
            return "ironic"
        return 'mixed'