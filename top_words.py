import json
from collections import Counter
import string

# defining stopwords
stopwords = {
    "the", "of", "and", "in", "a", "an", "to", "for", "at", "on", "as", "with",
    "by", "from", "–", "=", "|", "", "is", "was", "he", "she", "his", "her", "it",
    "who", "had", "that", "which", "this", "were", "but", "or", "when", "been",
    "be", "they", "their", "one", "into", "after", "where", "also", "new", "only",
    
    "january", "february", "march", "april", "may", "june", "july",
    "august", "september", "october", "november", "december",
    "years", "first", "second", "many", "most", "two",

    "university", "college", "school", "science", "scientific", "professor",
    "research", "work", "field", "received", "known", "studied", "made",
    "published", "education", "physicist", "mathematician", "chemist",

    "birth_place", "death_place", "death_date", "alma_mater", "doctoral_advisor",
    "doctoral_students", "signature", "citizenship", "residence", "nationality",
    "footnotes", "influenced", "influences", "spouse", "awards", "prizes", "award",
    "curie", "noether", "structure", "nuclear", "cambridge", "paris", "england",
    "london", "french", "german", "american", "italian", "history", "medal",
    "name", "work", "life", "woman", "female", "male", "man", "husband", "wife",
    "mother", "father", "children", "education", "national", "modern", "published",
    "society", "theory", "known_for", "de", "ibn", "wrote", "died", "born", "prize"
}

# loading the data
data = []
with open("cleaned.json", "r", encoding = "utf-8") as f:
    for line in f:
        try:
            data.append(json.loads(line))
        except json.JSONDecodeError as e:
            print("Skipping line due to error:", e)
            
print(f"Loaded {len(data)} entries.")

# tokenization and word collection

def clean_and_tokenize(text):
    words = text.lower().split()
    clean_words = [
        word.strip(string.punctuation)
        for word in words
        if word.strip(string.punctuation) not in stopwords and word.strip(string.punctuation)
    ]
    return clean_words

male_words = Counter()
female_words = Counter()

for entry in data:
    if "gender" in entry and "intro" in entry:
        tokens = clean_and_tokenize(entry["intro"])
        
        if entry["gender"] == "male":
            male_words.update(tokens)
            
        if entry["gender"] == "female":
            female_words.update(tokens)
            
print("\nTop 500 words for males:")
print(male_words.most_common(500))

print("\nTop 500 words for females:")
print(female_words.most_common(500))