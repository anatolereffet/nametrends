import pandas as pd

df = (
    pd.read_csv("./data/dpt2020.csv", sep=";")
    .loc[lambda df: df["preusuel"] != "_PRENOMS_RARES"]
    .loc[lambda df: df["annais"] != "XXXX"]
    .sort_values("annais")
    .drop("sexe", axis=1)
)

print(df.columns)
