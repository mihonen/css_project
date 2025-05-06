import mwclient
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import pandas as pd
import os
import json
import threading
from concurrent.futures import ThreadPoolExecutor

# this script is used to scrape individual peoples wikipedia pages during the years  
# and save their introductions to json file

# CONFIG

OUTPUT_FILE = "data/scraped.json"
FEMALES_FILE = "data/female_scientists.csv"
MALES_FILE = "data/male_scientists.csv"
USER_AGENT = 'ComputationalSocialScienceResearchProject/0.1 ' # <- You could add your own contact email here too 


site = mwclient.Site('en.wikipedia.org', clients_useragent=USER_AGENT)


THREADS = 5 # Wikipedia didn't ratelimit me with this so it's probably safe but wouldn't recommend increasing more
WRITE_LOCK = threading.Lock()  

seed = 42
sample_size = 100 # we sample this amount from both females and males, full dataset has 1000 both

start_year = 2005  
interval_months = 3




def get_intro(text):
    soup = BeautifulSoup(text, 'html.parser')
    # Intro is before the first heading (==)
    return soup.get_text().split('==')[0].strip()


def append_revision(data):
    with WRITE_LOCK:
        with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')



def process_person(person):
    name = person["name"]
    gender = person["gender"]

    # print(f"Processing: {name}")

    page = site.pages[name]

    dt = datetime(start_year, 1, 1)
    end_dt = datetime.now()

    try:
        while dt < end_dt:
            dt_str = dt.strftime('%Y-%m-%dT%H:%M:%SZ')
            next_dt = dt + timedelta(days=30 * interval_months)
            next_dt_str = next_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

            revs = list(page.revisions(start=dt_str, end=next_dt_str, dir='newer', prop='timestamp|content'))

            if revs:
                rev = revs[0]
                content = rev.get('*', '')
                intro = get_intro(content)

                revision_data = {
                    "name": name,
                    "timestamp": rev["timestamp"],
                    "intro": intro,
                    "interval_start": dt_str,
                    "interval_end": next_dt_str,
                    "gender": person["gender"]
                }

                append_revision(revision_data)

            dt = next_dt

    except Exception as e:
        print(f"Error processing {name}: {e}")





def main():

    # Sample random women and men from the full dataset
    df_female = pd.read_csv(FEMALES_FILE, header=None, names=["name"])
    df_male = pd.read_csv(MALES_FILE, header=None, names=["name"])


    # include gender for later reference and convert to lists
    sampled_women = [{"name": name, "gender": "female"} for name in df_female.sample(n=sample_size, random_state=seed)["name"]]
    sampled_men = [{"name": name, "gender": "male"} for name in df_male.sample(n=sample_size, random_state=seed)["name"]]


    # combine data into one list
    all_sampled = sampled_women + sampled_men


    # start scraping the data
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        executor.map(process_person, all_sampled)




if __name__ == "__main__":
    main()













