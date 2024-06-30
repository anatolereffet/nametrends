import pandas as pd
import warnings

warnings.filterwarnings(
    "ignore",
    "Geometry is in a geographic CRS. Results from 'centroid' are likely incorrect.",
)

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
