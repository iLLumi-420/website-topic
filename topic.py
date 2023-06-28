import csv
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords


def clean_data(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def generate_N_grams(text, ngram=1):
    words = [
        word for word in text.split(" ") if word not in set(stopwords.words("english"))
    ]
    temp = zip(*[words[i:] for i in range(0, ngram)])
    ans = [" ".join(ngram) for ngram in temp]
    return ans


# def generate_total_ngram(notes, n):
#     total_ngram = []
#     for note in notes:
#         individual_ngram = generate_N_grams(note, n)
#         total_ngram += individual_ngram
#     return total_ngram


domains = []
notes = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        domains.append(row["ï»¿Domain"])
        notes.append(row["Note"])


notes = [clean_data(note) for note in notes]

# unigram = generate_total_ngram(notes, 1)
# bigram = generate_total_ngram(notes, 3)
trigram = [generate_N_grams(note, 3) for note in notes]


topic_mapping = {}
for domain, ngram in zip(domains, trigram):
    ngram_counts = Counter(ngram)
    sorted_ngrams = sorted(ngram_counts.items(), key=lambda x: x[1], reverse=True)
    most_frequent_ngram = sorted_ngrams[0][0]
    topic_mapping[domain] = most_frequent_ngram

filed_names = ['Domain', 'Topic']
with open('output.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=filed_names)
    writer.writeheader()
    for domain, topic in topic_mapping.items():
        writer.writerow({'Domain': domain, 'Topic': topic})
