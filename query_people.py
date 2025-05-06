import requests
import pandas as pd


# This script queries wikipedia DB for 1000 male and 1000 female scientists
# and saves both to separate csv files

def run_sparql_query(gender_id, limit=1000):
    query = f"""
    SELECT ?personLabel ?article WHERE {{
      VALUES ?occupation {{
        wd:Q901         # scientist
        wd:Q169470      # physicist
        wd:Q593644      # chemist
        wd:Q2374463     # biologist
        wd:Q170790      # chemist (again, often used)
        wd:Q189290      # mathematician
        wd:Q1622272     # geologist
        wd:Q22325155    # neuroscientist
      }}
      
      ?person wdt:P106 ?occupation .
      ?person wdt:P21 wd:{gender_id} .
      ?person wdt:P31 wd:Q5 .              # human
      ?person wdt:P570 ?dod .              # date of death
      FILTER(YEAR(?dod) < 2000)

      ?article schema:about ?person .
      ?article schema:isPartOf <https://en.wikipedia.org/> .

      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    LIMIT {limit}
    """

    url = "https://query.wikidata.org/sparql"
    headers = {"Accept": "application/sparql-results+json"}
    response = requests.get(url, params={'query': query}, headers=headers)
    response.raise_for_status()
    results = response.json()["results"]["bindings"]
    return [entry["personLabel"]["value"] for entry in results]

# Wikidata gender IDs
FEMALE_ID = "Q6581072"
MALE_ID = "Q6581097"

# Fetch names
female_scientists = run_sparql_query(FEMALE_ID, limit=1000)
male_scientists = run_sparql_query(MALE_ID, limit=1000)

# Save to CSV
pd.DataFrame(female_scientists, columns=["name"]).to_csv("data/female_scientists.csv", index=False)
pd.DataFrame(male_scientists, columns=["name"]).to_csv("data/male_scientists.csv", index=False)

print("Saved 1000 female and 1000 male scientists to CSV.")
