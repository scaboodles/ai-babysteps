#!/usr/bin/env python3
import nltk
sentence = "The quick brown fox jumps over the lazy dog"
tokens = nltk.word_tokenize(sentence)
tagged_words = nltk.pos_tag(tokens)
print(tagged_words)