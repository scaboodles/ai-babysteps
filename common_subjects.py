#!/usr/bin/env python3
from collections import Counter
from scrape_book import scrape_and_format

def get_subjects(scope):
    subjects = []
    for i in range(scope):
        data = scrape_and_format()
        subjects.extend(data[1]['subjects'])
        print(f"{data[0]} read for good book")
        if i%10 == 0:
            print(f'\n\n ~~~~~~ book {i} ~~~~~~~~~~\n\n')
    return subjects

def find_common_subs(search_len, top_n):
    subjects = get_subjects(search_len) 
    dracula = Counter(subjects)
    top10 = dracula.most_common(top_n)
    print(top10)

find_common_subs(1000, 10)