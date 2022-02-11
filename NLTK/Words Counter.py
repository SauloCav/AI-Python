#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import average
from nltk.corpus import gutenberg

texts = [ 'shakespeare-caesar.txt', 'shakespeare-hamlet.txt', 'shakespeare-macbeth.txt', ]

def Counter(words):
    count = {}
    for item in words:
        if (item in count):
            count[item] += 1
        else:
            count[item] = 1
    return count

for i in texts:
    words = gutenberg.words(i)
    sents = gutenberg.sents(i)

    words_count = len(words)
    sentences_count = len(sents)
    counter = Counter(words)
    non_repeats = len( [w for w, c in counter.items() if c == 1] )
    repeats = len( [w for w, c in counter.items() if c > 1] )
    average_sentences = average( [len(s) for s in sents] )

    print(f"\n{i}:")
    print(f" Words: {words_count}")
    print(f" Sentences: {sentences_count}")
    print(f" Unrepeated Words: {non_repeats}")
    print(f" Repeated Words: {repeats}")
    print(f" Average Words per Sentence: {average_sentences}")
