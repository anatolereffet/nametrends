from dash import html, dcc
import dash_vega_components as dvc
import dash_bootstrap_components as dbc


def create_layout(app):
    return html.Div(
        [
            html.H1("Bar Chart Race for Top 10 Prenoms"),
            dcc.Graph(id="graph-raceplot"),
            dcc.Graph(id="graph-raceplot_male"),
            dcc.Graph(id="graph-raceplot_female"),
        ]
    )
