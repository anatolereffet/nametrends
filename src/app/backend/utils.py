import pandas as pd
import warnings
warnings.filterwarnings("ignore", "Geometry is in a geographic CRS. Results from 'centroid' are likely incorrect.")

FRENCH_DEPARTMENTS = [
    "01",
    "02",
    "03",
    "04",
    "05",
    "06",
    "07",
    "08",
    "09",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25",
    "26",
    "27",
    "28",
    "29",
    "30",
    "31",
    "32",
    "33",
    "34",
    "35",
    "36",
    "37",
    "38",
    "39",
    "40",
    "41",
    "42",
    "43",
    "44",
    "45",
    "46",
    "47",
    "48",
    "49",
    "50",
    "51",
    "52",
    "53",
    "54",
    "55",
    "56",
    "57",
    "58",
    "59",
    "60",
    "61",
    "62",
    "63",
    "64",
    "65",
    "66",
    "67",
    "68",
    "69",
    "70",
    "71",
    "72",
    "73",
    "74",
    "75",
    "76",
    "77",
    "78",
    "79",
    "80",
    "81",
    "82",
    "83",
    "84",
    "85",
    "86",
    "87",
    "88",
    "89",
    "90",
    "91",
    "92",
    "93",
    "94",
    "95",
    "971",
    "972",
    "973",
    "974",
]

POSSIBLE_YEARS = [str(year) for year in range(1900, 2021)]


def add_missing_departments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usable after a filter on a specific name & year,
    adds any french departments where the name hasn't occured in that year
    and sets the number of births to 0.

    Args:
        df (pd.DataFrame): filtered dataframe
    """
    existing_dpts = df["dpt"].unique()
    missing_dpts = sorted(
        [str(dpt) for dpt in FRENCH_DEPARTMENTS if dpt not in existing_dpts]
    )
    length = len(missing_dpts)
    tmp_df = pd.DataFrame(
        {
            "sexe": [df["sexe"].iloc[0]] * length,
            "prenoms": [df["prenoms"].iloc[0]] * length,
            "annee": [df["annee"].iloc[0]] * length,
            "dpt": missing_dpts,
            "nombre": [0] * length,
        }
    )
    result_df = pd.concat([df, tmp_df]).reset_index().drop(columns=["index"])

    return result_df


def add_missing_years(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usable after a filter on a specific name
    adds any year where the name hasn't occured in that year
    and sets the number of births to 0.

    Args:
        df (pd.DataFrame): filtered dataframe
    """

    existing_dpts = df["annee"].unique()

    missing_years = sorted(
        [str(dpt) for dpt in POSSIBLE_YEARS if dpt not in existing_dpts]
    )

    tmp_df = pd.DataFrame(
        {
            "annee": missing_years,
            "nombre": [0] * len(missing_years),
        }
    )
    result_df = pd.concat([df, tmp_df]).reset_index().drop(columns=["index"])

    return result_df


def precompute_data(names, regions, gender):
    """
    Precompute the most common names for each year and specified gender.

    Parameters:
    - names: GeoDataFrame with names data.
    - regions: GeoDataFrame with regions data.
    - gender: int, 1 for male and 2 for female names.

    Returns:
    - Dictionary with precomputed data for each year.
    """
    # IDF departments
    IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]

    precomputed_results = {}

    years = names["annee"].unique()
    for year in years:
        # Filter data for given year and specified gender
        filtered_data = names[(names["annee"] == year) & (names["sexe"] == gender)]

        # Find most common name in each dpt
        most_common_in_dpt = filtered_data.loc[filtered_data.groupby("dpt")["nombre"].idxmax()]

        # Calc centroid
        most_common_in_dpt["long"] = most_common_in_dpt.geometry.centroid.x
        most_common_in_dpt["lat"] = most_common_in_dpt.geometry.centroid.y
        idf_only = most_common_in_dpt[most_common_in_dpt["dpt"].isin(IDF)]

        # Specific processing for IDF
        most_common_name_idf = idf_only.groupby("prenoms")["nombre"].sum().idxmax()
        most_common_idf = idf_only[idf_only["prenoms"] == most_common_name_idf]

        # Copy & update regions DataFrame
        regions_copy = regions.copy()
        regions_copy["prenoms"] = most_common_name_idf
        regions_copy["nombre"] = most_common_idf["nombre"].sum()
        regions_copy["sexe"] = most_common_idf["sexe"].mode().iloc[0]
        regions_copy["long"] = regions_copy.geometry.centroid.x
        regions_copy["lat"] = regions_copy.geometry.centroid.y
        regions_copy["dpt"] = "IDF"

        # Combine IDF & non-IDF data
        combined_data = pd.concat(
            [most_common_in_dpt[~most_common_in_dpt["dpt"].isin(IDF)], regions_copy])

        # Storing precomputed data
        precomputed_results[year] = {
            "combined_data": combined_data,
            "idf_only": idf_only
        }

    return precomputed_results
