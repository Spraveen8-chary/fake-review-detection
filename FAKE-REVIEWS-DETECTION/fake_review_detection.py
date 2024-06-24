import re
from textblob import TextBlob

def preprocess(x):
    x = x.replace(",000,000", " m").replace(",000", " k").replace("′", "'").replace("’", "'")\
                           .replace("won't", " will not").replace("cannot", " can not").replace("can't", " can not")\
                           .replace("n't", " not").replace("what's", " what is").replace("it's", " it is")\
                           .replace("'ve", " have").replace("'m", " am").replace("'re", " are")\
                           .replace("he's", " he is").replace("she's", " she is").replace("'s", " own")\
                           .replace("%", " percent ").replace("₹", " rupee ").replace("$", " dollar ")\
                           .replace("€", " euro ").replace("'ll", " will").replace("how's"," how has").replace("y'all"," you all")\
                           .replace("o'clock"," of the clock").replace("ne'er"," never").replace("let's"," let us")\
                           .replace("finna"," fixing to").replace("gonna"," going to").replace("gimme"," give me").replace("gotta"," got to").replace("'d"," would")\
                           .replace("daresn't"," dare not").replace("dasn't"," dare not").replace("e'er"," ever").replace("everyone's"," everyone is")\
                           .replace("'cause'"," because")
    
    x = re.sub(r"([0-9]+)000000", r"\1m", x)
    x = re.sub(r"([0-9]+)000", r"\1k", x)
    x=re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))',' ',x)
    x=re.sub(r"\\s*\\b(?=\\w*(\\w)\\1{2,})\\w*\\b",' ',x)
    x=re.sub(r'<.*?>',' ',x)
    x=re.sub('[^a-zA-Z]',' ',x)

    return x

def score_classify(x):
    if x>3:
        return 'Positive'
    elif x<3:
        return 'Negative'
    else:
        return 'Neutral'
    
def analyze_sentiments(cleaned_verified_reviews):
    analysis=TextBlob(cleaned_verified_reviews)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity < 0:
        return 'Negative'
    else:
        return 'Neutral'

def predict(user_review, user_score):
    user_score_senti = score_classify(user_score)
    user_review = user_review.lower()
    user_review = user_review.replace('[^\w\s]', '')
    user_review = preprocess(user_review)

    if user_review == '':
        print('Please Enter some review')
        return 'Please Enter some review'
    elif analyze_sentiments(user_review) == 'Neutral' or user_score_senti == 'Neutral':
        print('Review Submitted! Genuine')
        return 'Review Submitted! Genuine'
    elif analyze_sentiments(user_review) == user_score_senti:
        print('Review Submitted! Genuine')
        return 'Review Submitted! Genuine'
    elif analyze_sentiments(user_review) != user_score_senti:
        print('Review Submitted! Not Genuine. Please recheck your review.')
        return 'Review Submitted! Not Genuine. Please recheck your review.'


# predict(user_review="The product is good", user_score=3)