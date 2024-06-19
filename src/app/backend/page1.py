from dash import Input, Output
import altair as alt
import pandas as pd


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
        names = app.dpd_table
        names.annee = names.annee.astype(int)
        year = names.loc[(names["annee"] >= 2000) & names["sexe"] == 1]

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
            alt.Color("prenoms:N", scale=alt.Scale(scheme="accent")),
            alt.value("lightgray"),
        )

        map_w_idf = (
            alt.Chart(subset_w_idf)
            .mark_geoshape(stroke="black")
            .encode(tooltip=["prenoms", "nom","code", "nombre"], color=color_condition)
            .properties(width=666, height=500)
            .add_params(single)
            # .add_selection(single)
        )


        map_idf_only = (
            alt.Chart(idf_only)
            .mark_geoshape(stroke="black")
            .encode(
                tooltip=["prenoms", "nom", "code", "nombre"],
                color=color_condition,
                text="prenoms",
            )
            .properties(width=333, height=250)
            .add_params(single)
            # .add_selection(single)
        )


        spacer = (
            alt.Chart().mark_text().encode(text=alt.value("")).properties(height=125)
        )

        centered_map_idf = alt.vconcat(spacer, map_idf_only, spacer)
        fig = (map_w_idf) | centered_map_idf

        # print(fig.to_dict())

        return [fig.to_dict()]
