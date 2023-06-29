import csv
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text


def generate_ngrams(text, n):
    words = [
        word for word in re.split(r"\s+", text.strip()) if word not in set(stopwords.words("english"))
    ]
    temp = zip(*[words[i:] for i in range(0, n)])
    ans = [" ".join(ngram) for ngram in temp]
    return ans

def filtered_ngrams(ngrams, most_frequent_ngrams):
    return [ngram for ngram in ngrams if ngram in most_frequent_ngrams]

def get_most_frequent_ngrams(notes, n):
    all_ngrams = []
    for note in notes:
        ngrams = generate_ngrams(note, n)
        all_ngrams.extend(ngrams)
    ngram_count = Counter(all_ngrams)
    most_frequent_ngrams = [ngram for ngram, count in ngram_count.most_common(100)]
    return most_frequent_ngrams



domains = []
notes = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        domains.append(row["ï»¿Domain"])
        notes.append(row["Note"])


cleaned_notes = [clean_text(note) for note in notes]

most_frequent_unigram = get_most_frequent_ngrams(cleaned_notes, 1)
most_frequent_bigram = get_most_frequent_ngrams(cleaned_notes, 2)
most_frequent_trigram = get_most_frequent_ngrams(cleaned_notes, 3)

# print(most_frequent_unigram)
# print(most_frequent_bigram)
# print(most_frequent_trigram)

topic_mapping = {}
for domain, note in zip(domains, cleaned_notes):
    # unigram = generate_ngrams(note, 1)
    bigram = generate_ngrams(note, 2)
    trigram = generate_ngrams(note, 3)

    # filtered_unigram = filtered_ngrams(unigram, most_frequent_unigram)
    filtered_bigram = filtered_ngrams(bigram, most_frequent_bigram)
    filtered_trigram = filtered_ngrams(trigram, most_frequent_trigram)



    all_ngrams =  filtered_bigram + filtered_trigram 

    if all_ngrams:
        ngram_counts = Counter(all_ngrams)
        most_frequent_ngram = ngram_counts.most_common(1)[0][0]
    else:
        most_frequent_ngram = "Unknown"

    topic_mapping[domain] = most_frequent_ngram


  
filed_names = ['Domain', 'Topic']
with open('output.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=filed_names)
    writer.writeheader()
    for domain, topic in topic_mapping.items():
        writer.writerow({'Domain': domain, 'Topic': topic})
