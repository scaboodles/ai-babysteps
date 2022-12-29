#!/usr/bin/env python3
import os
import regex as re
import random

def run():
    text, title, author, book_num= find_good_book()
    print(title, author, book_num)

def find_good_book():
    find_header = "START OF THE PROJECT GUTENBERG EBOOK.*"
    find_title = r"(?<=Title: ).*"
    find_auth = r"(?<=Author: ).*"

    while True:
        book_number = random.randint(11, 49987)
        text = get_book(book_number)

        title_match = re.search(find_title, text)
        author_match = re.search(find_auth, text)
        header_match = re.search(find_header, text)

        if(title_match and author_match and header_match):
            return text[(header_match.span()[1]):],title_match.group(),author_match.group(),book_number

def get_book(num):
    txt = os.popen(f"curl https://www.gutenberg.org/cache/epub/{num}/pg{num}.txt").read()
    return txt

run()