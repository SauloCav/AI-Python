import pandas as pd
import numpy as np
from textblob import TextBlob, Word, Blobber

print("\nnegative_words.csv: ")
file=open("negative_words.csv");
t=file.read();
text = TextBlob(t)
print(text.sentiment)

print('\n')
print('\n')

print("positive_words.csv: ")
file=open("positive_words.csv");
t=file.read();
text = TextBlob(t)
print(text.sentiment)
