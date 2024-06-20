import pandas as pd
import json


def load_babynames():
    return pd.read_csv(
        ".\\data\\dpt2020.csv",
        sep=";",
        dtype={"sexe": int, "prenoms": str, "dpt": str, "annee": str, "nombre": int},
    )


def load_map():
    with open(".\\data\\departement_avec_outremer_rapprochee.geojson") as response:
        depts = json.load(response)
    return depts
