import pandas as pd
from clean import clean
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import re
import string

#returns the most prevalent sentiment of the book
def get_sentiment(num):
    data = pd.DataFrame(columns=['sentences'])

    #open txt
    txt = ''
    with open(f'books/{num}.txt') as f:
        txt = f.read() #string
    txt = txt.split('.')  #list


    #clean txt
    chapterOneIndex = -1
    endIndex = len(txt)
    for i in range(len(txt)):
        if "CHAPTER I" in txt[i]: # only works for this specific book! i'm gonna use it anyway
            chapterOneIndex = i
        if "END OF THE PROJECT GUTENBERG EBOOK" in txt[i]:
            endIndex = i
            break
    data["sentences"] = txt[chapterOneIndex+1: endIndex]
    data["sentences"] = data["sentences"].apply(clean)

    #get sentiment of each sentence
    nltk.download('vader_lexicon')
    sentiments = SentimentIntensityAnalyzer()
    data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["sentences"]]
    data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["sentences"]]
    data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["sentences"]]
    data = data[["sentences", "Positive", "Negative", "Neutral"]]
    print(data.head())
    total_sum = len(data)

    #get average of each sentiment
    positive = data["Positive"].sum()/total_sum
    neutral = data["Neutral"].sum()/total_sum
    negative = data["Negative"].sum()/total_sum

    #print all sentiment values
    print("Positive: " + str(positive), "Neutral: " + str(neutral), "Negative: " + str(negative))

    #return most prevalent sentiment
    top_sentiment = max(positive, neutral, negative)
    if (top_sentiment == positive):
        return "positive"
    elif (top_sentiment == neutral):
        return "neutral"
    else:
        return "negative"
    
print(get_sentiment(21914))