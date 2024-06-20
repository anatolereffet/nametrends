import pandas as pd
import json
import os


def load_babynames():
    return pd.read_csv(
        os.path.join(".", "data", "dpt2020.csv"),
        sep=";",
        dtype={"sexe": int, "prenoms": str, "dpt": str, "annee": str, "nombre": int},
    )


def load_map():
    with open(
        os.path.join(".", "data", "departement_avec_outremer_rapprochee.geojson")
    ) as response:
        depts = json.load(response)
    return depts
