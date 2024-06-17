import pandas as pd

df = (
    pd.read_csv("./data/dpt2020.csv", sep=";")
    .rename(columns={"annais": "annee", "preusuel": "prenoms"})
    .loc[lambda df: df["prenoms"] != "_PRENOMS_RARES"]
    .loc[lambda df: df["annee"] != "XXXX"]
    .loc[lambda df: df["dpt"] != "XX"]
    .sort_values("annee")
    .drop("sexe", axis=1)
)

print(df.columns)
