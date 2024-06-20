import json
import pandas as pd
import os
from pathlib import Path


def main():
    data_folder = Path("./data/")
    df = pd.read_csv(data_folder / "dpt2020.csv", sep=";")

    if "XX" in df.dpt.unique():
        df = (
            df.rename(columns={"annais": "annee", "preusuel": "prenoms"})
            .loc[lambda df: df["prenoms"] != "_PRENOMS_RARES"]
            .loc[lambda df: df["annee"] != "XXXX"]
            .loc[lambda df: df["dpt"] != "XX"]
            .loc[lambda df: df["prenoms"].str.len() > 1]
            .sort_values("annee")
        )
        df.to_csv(data_folder / "dpt2020.csv", sep=";", index=False)
    else:
        print("Skip dpt2020.csv cleaning")

    df.loc[len(df.index)] = {"annee": "1997", "dpt": "75", "sexe": 1,
                             "prenoms": "ALEKSANDER", "nombre": 1}
    df = df.sort_values(by='annee').reset_index(drop=True)

    # IDF geojson
    with open(os.path.join("data", "idf.geojson"), "r") as file:
        geo_data = json.load(file)

    if len(geo_data["features"]) != 1:
        # Load only if it wasn't already cleaned
        # Departments geojson, correction of corsica
        data_path = os.path.join(
            "data", "departement_avec_outremer_rapprochee.geojson")
        with open(data_path, "r") as file:
            dpt_data = json.load(file)

        dpt_data["features"] = [
            french_dept
            for french_dept in dpt_data["features"]
            if french_dept["properties"]["code"] not in ["2A", "2B"]
        ]

        # Reassign the right department code for Corsica
        geo_data["features"][12]["properties"]["code"] = "20"
        # Add the corsica dpt to dpt files
        dpt_data["features"].append(geo_data["features"][12])

        # Filter on idf and full corsica polygon
        geo_data["features"] = [geo_data["features"][0]]
        # Rename the code to IDF
        geo_data["features"][0]["properties"]["code"] = "IDF"

        # Save the merged file
        with open(os.path.join("data", "departement_avec_outremer_rapprochee.geojson"), "w+") as f:
            json.dump(dpt_data, f, indent=2)

        with open(os.path.join("data", "idf.geojson"), "w+") as f:
            json.dump(geo_data, f, indent=2)
    else:
        print("Skipped geojson cleaning")


if __name__ == "__main__":
    main()
