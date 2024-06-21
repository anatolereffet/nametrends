from dash import html, dcc
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def create_layout(app):
    layout = html.Div(
        [
            html.H1("Altair Maps"),
            html.P("Replica of homepage but in Altair"),
            dbc.Stack(
                [
                    dmc.SegmentedControl(
                        id="gender-control",
                        value="male",
                        data=[
                            {"value": "male", "label": "Male"},
                            {"value": "female", "label": "Female"},
                        ],
                        mb=10,
                    ),
                    html.Div(
                        dmc.Slider(
                            id="slider-altair-map",
                            value=1900,
                            min=1900,
                            max=2020,
                            step=1,
                            labelAlwaysOn=True,
                            updatemode="mouseup",
                        )
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
