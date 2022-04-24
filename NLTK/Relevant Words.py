from nltk import WordNetLemmatizer, FreqDist, sent_tokenize, word_tokenize, pos_tag
from cmath import log
from nltk.corpus import stopwords, gutenberg

texts = [ "austen-emma.txt", "carroll-alice.txt", "melville-moby_dick.txt", "shakespeare-caesar.txt", "shakespeare-hamlet.txt", ]
dict = { "NN": "n", "VB": "v", "JJ": "a", "RB": "r", }

def penn2wordnet(penn_tag):
    for t, v in dict.items():
        if penn_tag.startswith(t):
            return v
    return "n"

def text_process(data):
    lemma = WordNetLemmatizer()
    stopw = stopwords.words("english")
    proc = sent_tokenize(data)
    proc = [word_tokenize(s) for s in proc]
    proc = [pos_tag(s) for s in proc]
    proc = [wt for s in proc for wt in s]
    proc = [
        (w.lower(), penn2wordnet(t))
        for w, t in proc if w.isalpha() and w not in stopw
    ]
    proc = [lemma.lemmatize(w, t) for w, t in proc]
    return proc

def calc_tf_idf(freqdist, fd):
    tf_idfs = []
    for w in fd:
        tf = fd[w] / fd.N()
        n = len(freqdist)
        df = sum(1 for fd in freqdist if fd[w] > 0)
        idf = log((1 + n)/(1 + df)).real
        tf_idfs.append((w, tf * idf))
    tf_idfs.sort(key=lambda x: -x[1])
    return tf_idfs

freqdist = {}

for i in texts:
    text_processed = text_process(gutenberg.raw(i))
    freqdist[i] = FreqDist(text_processed)

for i, fd in freqdist.items():
    tf_idf = calc_tf_idf(freqdist.values(), fd)
    print(f"\n{i}:")
    for j in range(5):
        w, v = tf_idf[j]
        print(f"  Word {j+1}: {w} ({v} TF-IDF)")
