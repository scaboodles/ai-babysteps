import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf #problematic line
from langdetect import detect
import plotly.offline as pyoff
import plotly.graph_objs as go
from collections import defaultdict
#pyoff.init_notebook_mode()

bookdata_path = 'book_data.csv'
testdata_path = 'book_data18.csv'
book = pd.read_csv(bookdata_path)[0:100]
test = pd.read_csv(testdata_path)[0:100]
print(book.columns)
print("NICE")
print(len(book))
def remove_invalid_lang(df):
    invalid_desc_idxs=[]
    for i in df.index:
        try:
            a=detect(df.at[i,'book_desc'])
           # print(a)
        except:
            invalid_desc_idxs.append(i)
    
    df=df.drop(index=invalid_desc_idxs)
    return df
book = remove_invalid_lang(book)
test = remove_invalid_lang(test)


#mapping!
book['lang']=book['book_desc'].map(lambda desc: detect(desc))
test['lang']=test['book_desc'].map(lambda desc: detect(desc))

lang_lookup = pd.read_html('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')[0]
#print(lang_lookup)
# print(type(lang_lookup))
#print(lang_lookup.columns)
langpd = lang_lookup[['ISO language name','639-1']]
#langpd = lang_lookup[[0, 1]]
langpd.columns = ['language','iso']
#print(langpd)


#all this is doing is changing the language names
print("OO")
print(langpd['iso'])
print(book) 
def desc_lang(x):
    if x in list(langpd['iso']):
        print(langpd[langpd['iso'] == x]['language'])
        return langpd[langpd['iso'] == x]['language'].values[0]
    else:
        print("NIL?")
        return 'nil'
book['language'] = book['lang'].apply(desc_lang)
test['language'] = test['lang'].apply(desc_lang)
#only get the english ones
book = book[book['language']=='English']
test = test[test['language']=='English']

# def genre_count(x):
#     try:
#         return len(x.split('|'))
#     except:
#         return 0
# book['genre_count'] = book['genres'].map(lambda x: genre_count(x))
# plot_data = [
#     go.Histogram(
#         x=book['genre_count']
#     )
# ]
# plot_layout = go.Layout(
#         title='Genre distribution',
#         yaxis= {'title': "Frequency"},
#         xaxis= {'title': "Number of Genres"}
#     )
# fig = go.Figure(data=plot_data, layout=plot_layout)
# pyoff.iplot(fig)

def genre_listing(x):
    try:
        lst = [genre for genre in x.split("|")]
        return lst
    except: 
        return []
print("OH")
book['genre_list'] = book['genres'].map(lambda x: genre_listing(x))
book['genre_list2'] = book['genres'].apply(genre_listing)
test['genre_list'] = book['genres'].map(lambda x: genre_listing(x))

print(book['genre_list'])
print(book['genre_list2'])

print("UH OH")

genre_dict = defaultdict(int)
for idx in book.index:
    g = book.at[idx, 'genre_list']
    if type(g) == list:
        for genre in g:
            genre_dict[genre] += 1
genre_pd = pd.DataFrame.from_records(sorted(genre_dict.items(), key=lambda x:x[1], reverse=True), columns=['genre', 'count'])


# plot_data = [
#  go.Bar(
#  x=genre_pd['genre'],
#  y=genre_pd['count']
#  )
# ]
# plot_layout = go.Layout(
#  title='Distribution for all Genres',
#  yaxis= {'title': 'Count'},
#  xaxis= {'title': 'Genre'}
#  )
# fig = go.Figure(data=plot_data, layout=plot_layout)
# pyoff.iplot(fig)


def determine_fiction(x):
    lower_list = [genre.lower() for genre in x]
    if 'fiction' in lower_list:
        return 'fiction'
    elif 'nonfiction' in lower_list:
        return 'nonfiction'
    else:
        return 'others'
book['label'] = book['genre_list'].apply(determine_fiction)
test['label'] = test['genre_list'].apply(determine_fiction)

