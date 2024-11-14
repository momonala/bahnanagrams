import re
from functools import lru_cache

import pandas as pd
import requests
from anagramgen import anagramgen
from bs4 import BeautifulSoup

url = "https://raw.githubusercontent.com/avandekleut/anagramgen/refs/heads/master/anagramgen/corpuses/top-3k.txt"
response = requests.get(url)
response.raise_for_status()
corpus = response.text
corpus = list(filter(lambda x: len(x) > 1, corpus.split()))

gen = anagramgen.AnagramGenerator(corpus)


@lru_cache
def best_anagram(word):
    anagrams = sorted(gen.generate(word), key=len)
    if anagrams:
        best_anagram = " ".join(anagrams[0])
        print(word, best_anagram)
        return best_anagram


url = "https://de.wikipedia.org/wiki/Liste_der_Berliner_U-Bahnh%C3%B6fe"
response = requests.get(url)
response.raise_for_status()
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find_all("table", {"class": "wikitable"})
df = pd.read_html(str(table[1]))[0]
pattern = r"^(.*?)\s\((.*?)\)\s+(\d+°\s\d+′\s\d+″\s[NS]),\s+(\d+°\s\d+′\s\d+″\s[EO])$"


def parse_station_info(station_str):
    match = re.match(pattern, station_str)
    if match:
        name, abbreviation, lat, long = match.groups()
        return pd.Series([name.strip(), abbreviation.strip(), lat, long])
    else:
        return pd.Series([None, None, None, None])


def normalize_station_name(station_name: str) -> str:
    station_name = station_name.lower()  # Convert to lowercase
    station_name = station_name.replace("ä", "ae")
    station_name = station_name.replace("ö", "oe")
    station_name = station_name.replace("ü", "ue")
    station_name = station_name.replace("ß", "ss")
    station_name = station_name.replace("-", " ")
    return station_name


df[['Station', 'Abbreviation', 'Latitude', 'Longitude']] = df['Bahnhof (Kürzel)  Karte'].apply(parse_station_info)
df['Station'] = df['Station'].apply(normalize_station_name)
df = df.drop_duplicates(subset='Station', keep='first')

df = df[[
    'Station',
    'Abbreviation',
    'Latitude',
    'Longitude',
    'Bahnhof (Kürzel)  Karte',
    # 'Linie',
    # 'Eröffnung',
    # 'Lage',
    'Ortsteil',
    # 'Umstieg',
    # 'Denkmal',
    # 'Anmerkungen',
    # 'Sehenswürdigkeiten',
    # 'Bild',

]]

df = df.dropna(subset=['Station'])

# df["anagram"] = df.Station.apply(best_anagram)
# df.to_csv("anagrams.csv")