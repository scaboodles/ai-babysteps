import numpy as np
import pandas as pd
import re
from scrape_book import scrape_and_format as owen_data
from sklearn.model_selection import train_test_split as tts
from tensorflow.keras.layers import LSTM, Embedding, Dropout, Dense
from tensorflow.keras import Sequential


# create df and vocabulary outside of init_df so it can be used globally.
df = pd.DataFrame(columns=["text", "subjects", "title", "author"])
vocabulary=set()
def init_df(num_books, text_len):
    global df
    for i in range(num_books):
        print(i+1)
        _, data_point = owen_data()
       # text, subjects, title, author = data_point
        with open(data_point["text"] + '.txt') as f:
            text = f.read()#[0:text_len]
            #print(data_point["title"])
            #print(text[0:5000])
            #endCommon = re.search(r"START OF THE PROJECT GUTENBERG EBOOK.*\*\*\*", text).end()#((CHAPTER 1)|(CHAPTER I).*(CHAPTER 1)|(CHAPTER I))?", data_point["text"])
            endRare = [x for x in re.finditer(r"(CHAPTER 1)|(CHAPTER I[/./w])|(Chapter 1)|(Chapter I[/./w])|(PART 1)|(PART I[/./w])|(Part 1)|(Part I[/./w])|(BOOK 1)|(BOOK I[/./w])|(Book 1)|(Book I[/./w])", text)]
            if len(endRare) != 0:
                data_point["text"] = text[endRare[-1].end(): endRare[-1].end()+text_len]
            else:
                data_point["text"] = text[0:text_len]

        for subject in data_point["subjects"]:
            if "fiction" in subject:
                data_point["subjects"] = "fiction"
                break
        if type(data_point["subjects"]) == list:
            data_point["subjects"] = "nonfiction"   
        print("DATA POINT") 
        print(data_point)   
        dfRow = pd.DataFrame(data_point, index=[0])
        df = df.append(dfRow)

def cleanText(text):
    text = text.lower()
    text = re.sub(r"what's", "what is ", text)
    text = text.replace('(ap)', '')
    text = re.sub(r"\'s", " is ", text)
    text = re.sub(r"\'ve", " have ", text)
    text = re.sub(r"can't", "cannot ", text)
    text = re.sub(r"n't", " not ", text)
    text = re.sub(r"i'm", "i am ", text)
    text = re.sub(r"\'re", " are ", text)
    text = re.sub(r"\'d", " would ", text)
    text = re.sub(r"\'ll", " will ", text)
    text = re.sub(r'\W+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\'", "", text)    
    text = re.sub(r"\"", "", text)
    text = re.sub('[^a-zA-Z ?!]+', '', text)
    text = "".join(i for i in text if ord(i)<128)
    text = text.strip()
    return text

#In order to tokenize, we have to first get a unique list of all the words.
def add_to_vocab(df):
    global vocabulary
    for book_text in df["text"]:
        for word in book_text.split():
            vocabulary.add(word)
    return vocabulary

def tokenize(text, vocab_dict, max_desc_length):
    # text_list = text.split(" ")
    # for word in text_list:
    #     if word in vocab_dict:
    #         word = vocab_dict[word]
    #     else:
    #         word = 0
    # return np.asarray(text_list)
    print("VOCAB DICT")
    print(vocab_dict)
    a=[vocab_dict[i] if i in vocab_dict else 0 for i in text.split()]
    b=[0] * max_desc_length
    print(len(a))
    if len(a)<max_desc_length:
        print("ACTUALLY HERE")
        return np.asarray(b[:max_desc_length-len(a)]+a).squeeze()
    else:
        print(text.split())
        print("SHOULD BE HERE")
        print(a)
        a = np.asarray(a[:max_desc_length]).squeeze()
        print(a.shape)
        print(a)
        return np.asarray(a[:max_desc_length]).squeeze()

#basically a split that allows us to keep half of the data..
def strat_split(df, target, val_percent):
    classes=list(df[target].unique())
    train_idxs, val_idxs = [], []
    for c in classes:
        idx=list(df[df[target]==c].index)
        np.random.shuffle(idx)
        val_size=int(len(idx)*val_percent)
        val_idxs+=idx[:val_size]
        train_idxs+=idx[val_size:]
    return train_idxs, val_idxs

def prepare_and_predict():
    global df
    text_length = 10000
    init_df(2000, text_length)
    df = df.rename(columns={'subjects': 'subject'})
    df["text"] = df["text"].apply(cleanText)

    add_to_vocab(df)
    vocab_dict={word: token+1 for token, word in enumerate(list(vocabulary))}
    token_dict={token+1: word for token, word in enumerate(list(vocabulary))}
    


    #tokenizing -- this is as simple as assigning a unique number to each word.
    df["text"] = df["text"].apply(tokenize, args=(vocab_dict, 250))

    #train_test_splitting
    train, test = tts(df, random_state=100, test_size = 0.2)

    classes=list(df.subject.unique())

    train_idxs, val_idxs = strat_split(train, 'subject', val_percent=0.2)

    print("SHAPES BEFORE")
    print(train[train.index.isin(train_idxs)]['text'].shape)
    print(train[train.index.isin(val_idxs)]['text'].shape)
    print(test["text"].shape)

    x_train=np.stack(train[train.index.isin(train_idxs)]['text'])
    y_train=train[train.index.isin(train_idxs)]['subject'].apply(lambda x:classes.index(x))
    x_val=  np.stack(train[train.index.isin(val_idxs)]['text'])
    y_val=train[train.index.isin(val_idxs)]['subject'].apply(lambda x:classes.index(x))

    #print(x_test.shape)

    print("X TEST BEFORE")
    print(test['text'])
    x_test= np.stack(test['text'])
    y_test=test['subject'].apply(lambda x:classes.index(x))
    #model creation n' training

    print(x_train.shape)
    print(x_train)
    print(y_train.shape)
    print(x_val.shape)
    print(y_val.shape)
    print("X TEST AFTER")
    print(x_test.shape)
    print(x_test)
    print(y_test.shape)
    

    parameters = {'vocab': vocabulary,
              'eval_batch_size': 30,
              'batch_size': 20,
              'epochs': 5,
              'dropout': 0.2,
              'optimizer': 'Adam',
              'loss': 'binary_crossentropy',
              'activation':'sigmoid'}
    BookModel1 = bookLSTM(x_train, y_train, x_val, y_val, x_test, y_test, parameters)


def bookLSTM(x_train, y_train, x_val, y_val, x_test, y_test, params):
    model = Sequential()
    #model.name="Book Model" it doesn't like model name setting :(
    model.add(Embedding(len(params['vocab'])+1, 250, input_length=250))# output_dim=x_train[0][0].shape, input_length=len(x_train[0][0])))
    model.add(LSTM(200, return_sequences=True))
    model.add(Dropout(params['dropout']))
    model.add(LSTM(200))
    model.add(Dense(1, activation=params['activation']))
    model.compile(loss=params['loss'],
              optimizer=params['optimizer'],
              metrics=['accuracy'])
    print(model.summary())
    model.fit(x_train, 
          y_train,
          validation_data=(x_val, y_val),
          batch_size=params['batch_size'], 
          epochs=params['epochs'])
    results = model.evaluate(x_test, y_test, batch_size=params['eval_batch_size'])
    print("RESULTS:")
    print(results)
    return model


#run time >:)
prepare_and_predict()

#print(df["text"][0:100])



# str = "ABECDE"
# matches = [x.start() for x in re.finditer("E", str)]
# print(matches[-1])