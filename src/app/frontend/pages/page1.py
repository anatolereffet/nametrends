from dash import html, dcc
import dash_vega_components as dvc
import dash_bootstrap_components as dbc


def create_layout(app):
    layout = html.Div(
        [
            html.H1("Altair Maps"),
            html.P("Replica of homepage but in Altair"),
            dbc.Stack(
                [
                    html.Div(
                        dcc.Slider(
                            id="slider-altair-map",
                            min=1900,  # till 1940, the map doesn't shift
                            max=2020,
                            value=1900,
                            marks={year: "" for year in range(1900, 2021, 1)},
                            tooltip={
                                "placement": "bottom",
                                "always_visible": True,
                                "style": {
                                    "font-style": "italic",
                                    "color": "White",
                                    "fontSize": "20px",
                                },
                            },
                            step=None,
                            updatemode="mouseup",
                        ),
                    ),
                    html.Div(
                        dvc.Vega(
                            id="graph-altair",
                            opt={"renderer": "canvas", "actions": False},
                        ),
                        className="centered_div",
                    ),
                ],
                gap=3,
            ),
        ]
    )
    return layout
