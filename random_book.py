#!/usr/bin/env python3
import os
import regex as re
import random

def run():
    text, title, author, book_num= find_good_book()
    #save_file = open(f"./books/{book_num}.txt",'w')
    #save_file.write(text)
    #save_file.close()
    return text, title, author, book_num

def find_good_book():
    find_header = "START OF THE PROJECT GUTENBERG EBOOK.*"
    find_title = r"(?<=Title: ).*"
    find_auth = r"(?<=Author: ).*"
    find_lang = r"(?<=Language: ).*"

    while True:
        book_number, text = get_book()

        title_match = re.search(find_title, text) #regex to find title, author, and header
        author_match = re.search(find_auth, text)
        header_match = re.search(find_header, text)
        lang = re.search(find_lang, text)

        if(title_match and author_match and header_match and lang): #if everything looks kosher return the book
            if lang.group() == "English":
                return text[(header_match.span()[1]):],title_match.group(),author_match.group(),book_number

def get_book():
    num = random.randint(11, 49987) #11 is the first non janky book, 49987 is the last
    try:
        txt = os.popen(f"curl https://www.gutenberg.org/cache/epub/{num}/pg{num}.txt").read() #curl to download plain text book
        return num, txt
    except:
        try:
            #print(f"decode error for book {num}, trying alternative url")
            txt = os.popen(f"curl https://www.gutenberg.org/cache/epub/{num}/{num}-0.txt").read() #curl to download plain text book
            return num, txt
        except:
            #print(f"failed curl for book {num}, trying different book")
            return get_book()