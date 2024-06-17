import pandas as pd
import json

def load_babynames():
    df = (
    pd.read_csv("./data/dpt2020.csv", sep=";")
    .rename(columns={"annais": "annee", "preusuel": "prenoms"})
    .loc[lambda df: df["prenoms"] != "_PRENOMS_RARES"]
    .loc[lambda df: df["annee"] != "XXXX"]
    .loc[lambda df: df["dpt"] != "XX"]
    .loc[lambda df: df["prenoms"].str.len() > 1]
    .sort_values("annee")
    )
    return df

def load_map():
    with open('./data/departement_avec_outremer_rapprochee.geojson') as response:
        depts = json.load(response)
    return depts