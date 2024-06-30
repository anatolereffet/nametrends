import plotly.express as px
from dash import Input, Output, dash_table
from backend.utils import add_missing_departments, add_missing_years
import pandas as pd
from itertools import product


def barchart(dataframe: pd.DataFrame, name: str):
    timeseries_data = dataframe.loc[dataframe["prenoms"] == name]

    timeseries_data = (
        timeseries_data.groupby(by=["annee"])
        .sum()
        .drop(columns=["prenoms", "sexe", "dpt"])
        .reset_index()
    )
    timeseries_data = add_missing_years(timeseries_data)
    timeseries_data.annee = timeseries_data.annee.astype(int)
    timeseries_data = timeseries_data.sort_values(by="annee")

    bchart = px.bar(timeseries_data, x="annee", y="nombre")
    return bchart


def lchart(dataframe, names):
    timeseries_data = dataframe.loc[dataframe["prenoms"].isin(names)]
    timeseries_data = (
        timeseries_data.groupby(by=["prenoms", "annee"])
        .sum()
        .drop(columns=["sexe", "dpt"])
        .reset_index()
    )
    timeseries_data = (
        timeseries_data.set_index(["annee", "prenoms"])
        .reindex(
            product(set(timeseries_data["annee"]), set(timeseries_data["prenoms"]))
        )
        .sort_index(level=1)
        .reset_index()
        .fillna(0)
    )
    timeseries_data.annee = timeseries_data.annee.astype(int)
    timeseries_data = timeseries_data.sort_values(by="annee")

    linechart = px.line(timeseries_data, x="annee", y="nombre", color="prenoms")

    return linechart


def home_callbacks(app):
    @app.callback(
        [
            Output("chartyear", "figure"),
        ],
        [Input("dropdown-names", "value")],
    )
    def update_bar_chart(names):
        # debug statements, ensure callback is called
        print(f"Selected name: {names}")
        babynames = app.df

        if len(names) == 1:
            names = names[0]
            chart = barchart(babynames, names)
        else:
            chart = lchart(babynames, names)

        return [chart]
