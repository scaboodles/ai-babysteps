import nltk
import re
nltk.download('stopwords')
stemmer = nltk.SnowballStemmer("english")
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
stopword=set(stopwords.words('english'))

lemmat = WordNetLemmatizer()


#note, this will first conver to lowercase
#then removes anything in brackets, <>s, punctuation, newlines, and numbers/words attached to numbers. 
#it also will REMOVE stopwords and stem (making it easier for further nltk)
def clean(text):
    text = str(text).lower()
    text = re.sub('\[.*?\]', '', text)  #if we have any brackets [] then it will remove brackets and anything inside.
    text = re.sub('https?://\S+|www\.\S+', '', text) #if we have an http, https, or a www url, it will remove the beginning and any non-whitespace that comes after.
    text = re.sub('<.*?>+', '', text) #if we have triangle brackets, it will remove anything inside and extra >s.
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #any brackets [] with a backslash and punctuation character inside.. (?)
    text = re.sub('\n+', ' ', text) #replace all newline characters with space
    text = re.sub(r'\t', '', text)
    text = re.sub('\w*\d\w*', '', text) #remove all digits, and if those digits are adjacent to word characters, remove the word characters too.
    text = [word for word in text.split(' ') if word not in stopword] #split the sentence by space and filter out stopwords.
    text=" ".join(text) #rejoin into one sentence
#    text = [stemmer.stem(word) for word in text.split(' ')] #split the sentence by space and filter out each word.
    text = [lemmat.lemmatize(word) for word in text.split(' ')]
    text=" ".join(text) #join the sentence back together
    return text