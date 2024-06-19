from dash import Input, Output
from src.app.backend.utils import add_missing_departments, add_missing_years
import altair as alt
import pandas as pd
from src.app.backend.utils import FRENCH_DEPARTMENTS


def add_empty_departments(
    table: pd.DataFrame, departments_polygons: pd.DataFrame
) -> pd.DataFrame:
    """
    Add the missing departments with the corresponding polygons.

    This is a hardcoded function for the year and sex
    will be fixed later

    Args:
        table (pd.DataFrame): filtered table
        departments_polygons (pd.DataFrame): dataframe holding code, name and shape of the departments

    Returns:
        pd.DataFrame: full table with missing polygons
    """
    missing_dpts = sorted(
        [str(dpt) for dpt in FRENCH_DEPARTMENTS if dpt not in table.dpt.unique()]
    )
    mia_dpts = {
        "code": missing_dpts,
        "nom": [],
        "geometry": [],
        "sexe": [1] * len(missing_dpts),
        "prenoms": [" "] * len(missing_dpts),
        "annee": [2000] * len(missing_dpts),
        "dpt": missing_dpts,
        "nombre": [0] * len(missing_dpts),
    }
    for dpt_code in missing_dpts:
        _, dpt_name, polygon_dpt = departments_polygons[
            departments_polygons["code"] == dpt_code
        ].squeeze()
        mia_dpts["nom"].append(dpt_name)
        mia_dpts["geometry"].append(polygon_dpt)

    df = pd.concat([table, pd.DataFrame(mia_dpts)]).reset_index()
    return df


def firstpage_callbacks(app):
    @app.callback(
        [
            Output("graph-altair", "spec"),
        ],
        [
            Input("dropdown-names_altair", "value"),
        ],
    )
    def update_altair_map(name):
        # debug statements, ensure callback is called
        print("Callback page1")
        print(name)
        data = app.df
        names = app.dpd_table
        depts_polygon_table = app.departments

        names.annee = names.annee.astype(int)
        year = names.loc[(names["annee"] >= 2000) & data["sexe"] == 1]

        year = add_empty_departments(year, depts_polygon_table)

        subset = year.loc[year.groupby("dpt")["nombre"].idxmax()]
        regions = app.regions

        # Separate IDF and province
        IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]
        subset.loc[:, "long"] = subset.geometry.centroid.x
        subset.loc[:, "lat"] = subset.geometry.centroid.y
        idf_only = subset.loc[subset.code.isin(IDF)]

        regions["prenoms"] = idf_only["prenoms"].max()
        regions["nombre"] = idf_only.loc[
            idf_only["prenoms"] == idf_only["prenoms"].max()
        ]["nombre"].sum()
        regions["sexe"] = idf_only.loc[
            idf_only["prenoms"] == idf_only["prenoms"].max()
        ]["sexe"].values[0]
        regions["long"] = regions["geometry"].centroid.x
        regions["lat"] = regions["geometry"].centroid.y
        regions["dpt"] = "IDF"
        subset_w_idf = pd.concat([subset.loc[~subset["code"].isin(IDF)], regions])

        # single = alt.selection_single()
        single = alt.selection_point()

        color_condition = alt.condition(
            single,
            alt.Color("nombre:Q", scale=alt.Scale(scheme="purplered")),
            alt.value("lightgray"),
        )

        map_w_idf = (
            alt.Chart(subset_w_idf)
            .mark_geoshape(stroke="black")
            .encode(tooltip=["prenoms", "code", "nombre"], color=color_condition)
            .properties(width=800, height=600)
            .add_params(single)
            # .add_selection(single)
        )

        text_w_idf = (
            alt.Chart(subset_w_idf)
            .mark_text(color="black", fontSize=10)
            .encode(latitude="lat", longitude="long", text="prenoms:N")
        )

        map_idf_only = (
            alt.Chart(idf_only)
            .mark_geoshape(stroke="black")
            .encode(
                tooltip=["prenoms", "nom", "code", "nombre"],
                color=color_condition,
                text="prenoms",
            )
            .properties(width=400, height=300)
            .add_params(single)
            # .add_selection(single)
        )

        text_idf_only = (
            alt.Chart(idf_only)
            .mark_text(color="black", fontSize=10)
            .encode(latitude="lat", longitude="long", text="prenoms:N")
        )

        spacer = (
            alt.Chart().mark_text().encode(text=alt.value("")).properties(height=175)
        )

        centered_map_idf = alt.vconcat(spacer, map_idf_only + text_idf_only, spacer)
        fig = (map_w_idf + text_w_idf) | centered_map_idf

        # print(fig.to_dict())

        return [fig.to_dict()]
