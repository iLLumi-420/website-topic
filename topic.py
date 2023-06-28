import csv
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords


def clean_data(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def generate_N_grams(text, n):
    words = [
        word for word in re.split(r"\s+", text.strip()) if word not in set(stopwords.words("english"))
    ]
    temp = zip(*[words[i:] for i in range(0, n)])
    ans = [" ".join(ngram) for ngram in temp]
    return ans

def get_total_ngrams(ngrams):
    total_ngrams = []
    for ngram in ngrams:
        total_ngrams += ngram
    return total_ngrams

domains = []
notes = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        domains.append(row["ï»¿Domain"])
        notes.append(row["Note"])


notes = [clean_data(note) for note in notes]

unigram = [generate_N_grams(note,1) for note in notes]

trigram = [generate_N_grams(note, 3) for note in notes]

total_unigram = get_total_ngrams(unigram)

total_unigram_count = Counter(total_unigram)
sorted_total_unigram = sorted(total_unigram_count.items(), key=lambda x:x[1], reverse=True)
most_frequent_unigram = sorted_total_unigram[:100]

# print(most_frequent_unigram)

# def updated_words(note_words):
#     if most_freq_note_words not in most_frequent_unigram:

topic_mapping = {}

for domain, ngram_note in zip(domains, unigram):
    for word in ngram_note:
        if word not in most_frequent_unigram:
            ngram_note.remove(word)
    ngram_counts = Counter(ngram_note)
    sorted_ngrams = sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)
    most_frequent_ngram = sorted_ngrams[0][0]
    most_freq_note_words = most_frequent_ngram.split()
    topic_mapping[domain] = most_frequent_ngram


   

filed_names = ['Domain', 'Topic']
with open('output.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=filed_names)
    writer.writeheader()
    for domain, topic in topic_mapping.items():
        writer.writerow({'Domain': domain, 'Topic': topic})
