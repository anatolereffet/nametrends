from dash import Output, Input
from raceplotly.plots import barplot


def bar_chart_race_callbacks(app):
    @app.callback(
        Output("graph-raceplot", "figure"),
        [Input("url", "pathname")]
    )
    def create_bar_chart_race(pathname):
        data = app.df
        grouped_df = data.groupby(['prenoms', 'annee'], as_index=False).sum()
        # Create bar plot race
        my_raceplot = barplot(grouped_df,
                              item_column='prenoms',
                              value_column='nombre',
                              time_column='annee')
        # Generate the race plot figure
        fig = my_raceplot.plot(title='Top 10 prenoms',
                               item_label='Top 10 prenoms',
                               value_label='nombre',
                               frame_duration=1000)
        return fig
