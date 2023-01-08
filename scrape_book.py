#!/usr/bin/env python3
from random_book import run 
from io import StringIO
from html.parser import HTMLParser
import os

def scrape_and_format():
    text, title, author, book_num = run() #use random_books run method to get a book
    subjects = get_subject_list(book_num)

    save_file = open(f"./books/{book_num}.txt",'w+') #this will write text to a file and will overwrite if that file already exists
    save_file.write(text)
    save_file.close() #data point has refers to text file by path

    data_point = {'text' : f"./books/{book_num}", 'subjects' : subjects, 'title' : title, 'author' : author} #compose data dict
    return book_num, data_point #scrape and format will return tuple of dictionary and book id

class MLStripper(HTMLParser): #class to strip html tags from curl request
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html): #utilizes MLStripper to clean up curl request
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def clean_page(txt): #format data neatly to scrape from
    stripped = strip_tags(txt)
    list = stripped.split('\n')
    while "" in list:
        list.remove("")
    return list

def data_curl(num): #get web page to scrape from
    web_pg = os.popen(f"curl https://www.gutenberg.org/ebooks/{num}").read()
    if isinstance(web_pg, bytes):  
        web_pg = web_pg.decode('utf-8')
    return web_pg

def scrape_subjects(stripped): #tie it all together and return subjects
    subjects = []
    for i in range(len(stripped)):
        if stripped[i].lower() == 'subject':
            subjects.append(stripped[i+1].lower().strip())

    #split up genre from sub-genres (denoted by -- on proj. gutenberg)
    joined = "--".join(subjects)
    subjects = joined.split('--')

    make_set = set(subjects) #make into a set to prevent dupes
    return list(make_set) #back into list to make it easier to work with

def get_subject_list(book_num):
    return scrape_subjects(clean_page(data_curl(book_num))) #quick one line method composition