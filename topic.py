import csv
import re
import nltk
from collections import Counter



def generate_ngrams(text, n):
    words = [
        word for word in re.split(r"\s+", text.strip()) 
    ]
    temp = zip(*[words[i:] for i in range(0, n)])
    ans = [" ".join(ngram) for ngram in temp]
    return ans

def filtered_ngrams(ngrams, most_frequent_ngrams):
    return [ngram for ngram in ngrams if ngram in most_frequent_ngrams]

def get_most_frequent_ngrams(notes):
    all_ngrams = []
    for note in notes:
        trigrams = generate_ngrams(note, 3)
        all_ngrams.extend(trigrams)
    ngram_count = Counter(all_ngrams)
    most_frequent_ngrams = [ngram for ngram, count in ngram_count.most_common(60)]
    print(most_frequent_ngrams)
    return most_frequent_ngrams




domains = []
notes = []
location = []

with open("data.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        domains.append(row["ï»¿Domain"])
        notes.append(row["Note"])
        state = row['Location'].lower()
        if state not in location:
            location.append(state)

def clean_text(text):
    text = text.lower()
    removed_state = ''

    cleaner_text = text.split('--')
    text = cleaner_text[0]

    unigram = generate_ngrams(text, 1)
    bigram = generate_ngrams(text, 2)
    trigram = generate_ngrams(text, 3)
    quadgram = generate_ngrams(text, 4)

    total_ngrams = unigram + bigram + trigram + quadgram

    
    for word in total_ngrams:
        if word in location:
            text = text.replace(word, '')
            removed_state = word
          
    text = re.sub(r"[^\w\s]", "", text)
    return [text, removed_state]

cleaned_notes_with_state = [clean_text(note) for note in notes]

most_frequent_ngrams = get_most_frequent_ngrams([notes[0] for notes in cleaned_notes_with_state])

topic_mapping = {}
for domain, note, original_note in zip(domains, cleaned_notes_with_state, notes):
    trigram = generate_ngrams(note[0], 3)



    all_ngrams = filtered_ngrams(trigram, most_frequent_ngrams)

    if all_ngrams:
        ngram_counts = Counter(all_ngrams)
        most_frequent_ngram = ngram_counts.most_common(1)[0][0]

    else:
        most_frequent_ngram = ""

    topic_mapping[domain] = [ most_frequent_ngram , original_note , note[1] ]

  
filed_names = ['Domain', 'Topic', 'State', 'Note']
with open('output.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames=filed_names)
    writer.writeheader()
    for domain, info in topic_mapping.items():
        writer.writerow({'Domain': domain, 'Topic': info[0], 'State': info[2], 'Note':info[1]})
    
