from dash import Output, Input
import numpy as np
import plotly.express as px


def sunburst_callbacks(app):
    @app.callback(
        Output("sunburst-plot", "figure"),
        [Input("slider-sunburst", "value")],
    )
    def create_sunburst(selected_year):
        data = app.df
        with open("./data/names.txt", "r") as file:
            # Read all lines into a list
            lines_list = file.readlines()
        names_bible = [line.strip() for line in lines_list]

        data = data.loc[data["annee"] == str(selected_year)]
        data["sexe"] = data["sexe"].map({2: "Female", 1: "Male"})
        data = data.groupby(by=["prenoms", "annee", "sexe"], as_index=False).agg(
            {"nombre": "sum"}
        )

        data["christian"] = data["prenoms"].map(
            lambda x: "Christian"
            if any(line in x for line in names_bible)
            else "Non-Christian"
        )
        data["top5"] = np.where(
            data.groupby("sexe")["nombre"].rank(method="first", ascending=False) <= 5,
            data["prenoms"],
            "Other",
        )

        fig = px.sunburst(
            data,
            path=["sexe", "christian", "top5"],
            values="nombre",
            color="christian",
            color_discrete_map={
                "Christian": "#636efa",
                "Non-Christian": "#ef553b",
            },
        )

        return fig
