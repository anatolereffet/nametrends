import plotly.express as px
from dash import Input, Output, dash_table
from backend.utils import add_missing_departments, add_missing_years


def home_callbacks(app):
    @app.callback(
        [
            Output("graph", "figure"),
            Output("chartyear", "figure"),
        ],
        [Input("dropdown-names", "value"), Input("dropdown-year", "value")],
    )
    def update_bar_chart(name, year):
        # debug statements, ensure callback is called
        print(f"Selected name: {name}")
        print(f"Selected year: {year}")
        departments = app.geojson
        babynames = app.df
        name = name.upper()
        year_filter = babynames.loc[babynames["annee"] == year]
        name_filter = year_filter.loc[year_filter["prenoms"] == name]
        timeseries_data = babynames.loc[babynames["prenoms"] == name]
        # if empty give single row df with name still at 0.
        name_filter.dpt = name_filter.dpt.astype(str)
        if len(name_filter.index) == 0:
            name_filter = name_filter.copy()
            name_filter.loc[0] = [1, name, year, "01", 0]

        if len(timeseries_data.index) == 0:
            # Handle year chart specifity
            timeseries_data = timeseries_data.copy()
            timeseries_data.loc[0] = [1, name, year, "01", 0]

        data = add_missing_departments(name_filter)

        timeseries_data = (
            timeseries_data.groupby(by=["annee"])
            .sum()
            .drop(columns=["prenoms", "sexe", "dpt"])
            .reset_index()
        )

        timeseries_data = add_missing_years(timeseries_data)
        timeseries_data.annee = timeseries_data.annee.astype(int)
        timeseries_data = timeseries_data.sort_values(by="annee")

        fig = px.choropleth(
            data_frame=data,
            geojson=departments,
            locations="dpt",
            color="nombre",
            featureidkey="properties.code",
            projection="mercator",
        )

        fig.update_geos(fitbounds="geojson", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, dragmode=False)

        chart = px.bar(timeseries_data, x="annee", y="nombre")
        return fig, chart
