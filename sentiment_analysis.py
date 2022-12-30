import pandas as pd
from textClean import clean
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import re
import string

data = pd.DataFrame(columns=['sentences'])

txt = ''
with open('./books/16954.txt') as f:
    txt = f.read() #string

txt = txt.split('.')  #list
#print(txt)

#now clean 

#first we want to make sure 
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

nltk.download('vader_lexicon')
sentiments = SentimentIntensityAnalyzer()
data["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in data["sentences"]]
data["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in data["sentences"]]
data["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in data["sentences"]]
data = data[["sentences", "Positive", "Negative", "Neutral"]]
print(data.head())
total_sum = len(data)
print("Positive: " + str(data["Positive"].sum()/total_sum), "Negative: " +str(data["Negative"].sum()/total_sum), "Neutral: " +str(data["Neutral"].sum()/total_sum))
