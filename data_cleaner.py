import json
import re
from bs4 import BeautifulSoup

# this script just cleans up links and such things from the scraped data

INPUT_FILE = 'data/scraped.json'
OUTPUT_FILE = 'data/cleaned.json'

def clean_intro(raw_text):
    # Remove HTML
    text = BeautifulSoup(raw_text, 'html.parser').get_text()

    # Remove Wikipedia-style bold/italic markup
    text = re.sub(r"''+", '', text)

    # Remove wiki-links but keep display text
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\2', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # Remove templates (e.g., {{...}})
    text = re.sub(r'\{\{[^\}]*\}\}', '', text)

    # Remove file/image embeds
    text = re.sub(r'\[\[File:[^\]]+\]\]', '', text, flags=re.IGNORECASE)

    # Collapse multiple newlines
    text = re.sub(r'\n+', '\n', text)

    # Strip leading/trailing whitespace
    return text.strip()

with open(INPUT_FILE, 'r', encoding='utf-8') as infile, open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
    for line in infile:
        try:
            entry = json.loads(line)
            entry['intro'] = clean_intro(entry['intro']) 
            json.dump(entry, outfile, ensure_ascii=False)
            outfile.write('\n')
        except Exception as e:
            print(f"[!] Error processing line: {e}")
