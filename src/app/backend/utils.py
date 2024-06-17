import pandas as pd

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


def add_missing_departments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Usable after a filter on a specific name & year,
    adds any french departments where the name hasn't occured in that year
    and sets the number of births to 0.

    Args:
        df (pd.DataFrame): filtered dataframe
    """
    return (
        df.pivot_table(
            index=["annee", "prenoms"], columns="dpt", values="nombre", fill_value=0
        )
        .reindex(
            columns=pd.Index(df["dpt"].unique()).union(FRENCH_DEPARTMENTS), fill_value=0
        )
        .reset_index()
        .melt(
            id_vars=["annee", "prenoms"],
            value_vars=FRENCH_DEPARTMENTS,
            var_name="dpt",
            value_name="nombre",
        )
        .sort_values(by=["annee", "prenoms", "dpt"])
        .reset_index(drop=True)
    )
