from dash import Output, Input
from raceplotly.plots import barplot


def bar_chart_race_callbacks(app):
    @app.callback(
        Output("graph-raceplot", "figure"),
        Output("graph-raceplot_male", "figure"),
        Output("graph-raceplot_female", "figure"),
        [Input("url", "pathname")],
    )
    def create_bar_chart_race(pathname):
        data = app.df
        grouped_df = data.groupby(["prenoms", "annee", "sexe"], as_index=False).agg(
            {"nombre": "sum"}
        )
        grouped_male = grouped_df.loc[grouped_df["sexe"] == 1]
        grouped_female = grouped_df.loc[grouped_df["sexe"] == 2]
        # Create bar plot race
        my_raceplot = barplot(
            grouped_df,
            item_column="prenoms",
            value_column="nombre",
            time_column="annee",
        )
        raceplot_m = barplot(
            grouped_male,
            item_column="prenoms",
            value_column="nombre",
            time_column="annee",
        )
        raceplot_f = barplot(
            grouped_female,
            item_column="prenoms",
            value_column="nombre",
            time_column="annee",
        )
        # Generate the race plot figure
        fig = my_raceplot.plot(
            title="Top 10 names global scale", value_label="number", frame_duration=1000
        )
        male_fig = raceplot_m.plot(
            title="Top 10 male names", value_label="number", frame_duration=1000
        )
        female_fig = raceplot_f.plot(
            title="Top 10 female names", value_label="number", frame_duration=1000
        )
        return fig, male_fig, female_fig
