import json
import pandas as pd

df = (
    pd.read_csv("./data/dpt2020.csv", sep=";")
    .rename(columns={"annais": "annee", "preusuel": "prenoms"})
    .loc[lambda df: df["prenoms"] != "_PRENOMS_RARES"]
    .loc[lambda df: df["annee"] != "XXXX"]
    .loc[lambda df: df["dpt"] != "XX"]
    .loc[lambda df: df["prenoms"].str.len() > 1]
    .sort_values("annee")
)

df.to_csv("./data/dpt2020.csv", sep=";", index=False)

# Departments geojson, correction of corsica
with open("./data/departement_avec_outremer_rapprochee.geojson", "r") as file:
    geo_data = json.load(file)

for french_dept in geo_data["features"]:
    if french_dept["properties"]["code"] in ["2A", "2B"]:
        french_dept["properties"]["code"] = "20"

with open("./data/departement_avec_outremer_rapprochee.geojson", "w+") as f:
    json.dump(geo_data, f, indent=2)

# IDF geojson
with open("./data/idf.geojson", "r") as file:
    geo_data = json.load(file)

# Filter on idf polygon
geo_data["features"] = [geo_data["features"][0]]
# Rename the code to IDF
geo_data["features"][0]["properties"]["code"] = "IDF"

with open("./data/idf.geojson", "w+") as f:
    json.dump(geo_data, f, indent=2)
