#!/usr/bin/env python3
import os
import regex as re

path = "./books"
files_list = os.listdir(path)

num_list = []
for file in files_list:
    num = int(re.sub('.txt', '', file))
    num_list.append(num)

num_list.sort()
checklist = []

for i in range(1,5000):
    checklist.append(i)


missing = []

for num in checklist:
    if not num in num_list:
        missing.append(num)

print(missing)