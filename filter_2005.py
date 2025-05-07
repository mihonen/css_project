import mwclient
import pandas as pd
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

INPUT_FEMALE = 'data/female_scientists.csv'
INPUT_MALE = 'data/male_scientists.csv'
OUTPUT_FEMALE = 'data/female_scientists_2005.csv'
OUTPUT_MALE = 'data/male_scientists_2005.csv'

THREADS = 4
USER_AGENT = 'ComputationalSocialScienceResearchProject/0.1 '

site = mwclient.Site('en.wikipedia.org', clients_useragent=USER_AGENT)

def has_2005_revision(name):
    try:
        page = site.pages[name]
        revs = list(page.revisions(start='2005-01-01T00:00:00Z', end='2005-12-31T23:59:59Z', dir='newer', prop='ids'))
        return name if revs else None
    except Exception as e:
        print(f"[!] Error with {name}: {e}")
        return None

def filter_names(names):
    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        results = list(executor.map(has_2005_revision, names))
    return [r for r in results if r is not None]

def main():
    df_female = pd.read_csv(INPUT_FEMALE)
    df_male = pd.read_csv(INPUT_MALE)

    print("Filtering female scientists...")
    filtered_female = filter_names(df_female["name"].tolist())
    pd.DataFrame(filtered_female, columns=["name"]).to_csv(OUTPUT_FEMALE, index=False)
    print(f"Saved {len(filtered_female)} to {OUTPUT_FEMALE}")

    print("Filtering male scientists...")
    filtered_male = filter_names(df_male["name"].tolist())
    pd.DataFrame(filtered_male, columns=["name"]).to_csv(OUTPUT_MALE, index=False)
    print(f"Saved {len(filtered_male)} to {OUTPUT_MALE}")

if __name__ == "__main__":
    main()
