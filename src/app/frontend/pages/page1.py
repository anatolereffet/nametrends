from dash import html, dcc
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def create_layout(app):
    layout = html.Div(
        [
            html.H1("Altair Maps : Highest given name in France by year and gender"),
            html.P("Select wether you want to check for male name or female given name. Then select the year you want to check. The map will show the most "
                   "given name in France for the selected year. You can pass your cursor over the map to see the name and the number of people who received it. "
                   "Note that we did not work on the unpopular names because there are too many names at 0 (the rarest names) and so it was for us unecessary "
                   "to select few of them at random."),
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
                gap=4,
            ),
        ]
    )
    return layout
