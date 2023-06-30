import csv
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords



def generate_ngrams(text, n):
    words = [
        word for word in re.split(r"\s+", text.strip()) if word not in set(stopwords.words("english"))
    ]
    temp = zip(*[words[i:] for i in range(0, n)])
    ans = [" ".join(ngram) for ngram in temp]
    return ans

def filtered_ngrams(ngrams, most_frequent_ngrams):
    return [ngram for ngram in ngrams if ngram in most_frequent_ngrams]

def get_most_frequent_ngrams(notes):
    all_ngrams = []
    for note in notes:
        bigrams = generate_ngrams(note, 2)
        trigrams = generate_ngrams(note, 3)
        all_ngrams.extend(bigrams)
        all_ngrams.extend(trigrams)
    ngram_count = Counter(all_ngrams)
    most_frequent_ngrams = [ngram for ngram, count in ngram_count.most_common(60)]
    return most_frequent_ngrams




domains = []
notes = []
location = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        domains.append(row["ï»¿Domain"])
        notes.append(row["Note"])
        if row["Location"] not in location:
            location.append(row["Location"].lower())

def clean_text(text):
    text = text.lower()
    removed_state = ''
    cleaner_text = text.split('--')
    text = cleaner_text[0]
    for state in location:
        if state in text:
            text = text.replace(state, '')
            removed_state = state


    text = re.sub(r"[^\w\s]", "", text)
    return [text, removed_state]


cleaned_notes_with_state = [clean_text(note) for note in notes]
most_frequent_ngrams = get_most_frequent_ngrams(cleaned_notes_with_state[0])


topic_mapping = {}
for domain, note in zip(domains, cleaned_notes_with_state):
 
    bigram = generate_ngrams(note[0], 2)
    trigram = generate_ngrams(note[0], 3)

    filtered_bigram = filtered_ngrams(bigram, most_frequent_ngrams)
    filtered_trigram = filtered_ngrams(trigram, most_frequent_ngrams)



    all_ngrams =  filtered_bigram + filtered_trigram 

    if all_ngrams:
        ngram_counts = Counter(all_ngrams)
        most_frequent_ngram = ngram_counts.most_common(1)[0][0]

    else:
        most_frequent_ngram = ""

    topic_mapping[domain] = [ most_frequent_ngram , note[0], note[1] ]


  
filed_names = ['Domain', 'Topic', 'State', 'Note']
with open('output.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=filed_names)
    writer.writeheader()
    for domain, info in topic_mapping.items():
        writer.writerow({'Domain': domain, 'Topic': info[0], 'State': info[2], 'Note':info[1]})
    
