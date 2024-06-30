from dash import html
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc


def create_layout(app):
    return html.Div(
        children=[
            dmc.Paper(
                className="graph-standalone-altair",
                shadow="sm",
                children=[
                    dmc.Center(
                        style={"height": "100%", "width": "100%"},
                        children=[
                            dvc.Vega(
                                id="graph-altair",
                                opt={"renderer": "canvas", "actions": False},
                                style={
                                    "height": "100%",
                                    "width": "100%",
                                },
                            )
                        ],
                    ),
                    dmc.Center(
                        children=[
                            dmc.Text(
                                "Select a year or an interval",
                                p=40,
                                weight=700,
                                italic=True,
                                size="xl",
                            ),
                        ],
                    ),
                    dbc.Stack(
                        [
                            dmc.RangeSlider(
                                id="slider-altair-map",
                                value=[1900, 1905],
                                min=1900,
                                max=2020,
                                minRange=0,
                                step=1,
                                labelAlwaysOn=True,
                                updatemode="mouseup",
                            ),
                            dmc.SegmentedControl(
                                id="gender-control",
                                value="male",
                                data=[
                                    {"value": "male", "label": "Male"},
                                    {"value": "female", "label": "Female"},
                                ],
                                mb=10,
                            ),
                        ]
                    ),
                ],
            ),
            dmc.Paper(
                className="text-explanation-altair",
                shadow="xl",
                children=[
                    dmc.Center(
                        children=[
                            dmc.Title(
                                "Geographical Overview",
                                order=1,
                            ),
                        ]
                    ),
                    dmc.Text(
                        "This interactive map of France explores the regional variations "
                        "in name popularity across different years and genders. By selecting "
                        "a specific year (or interval) and gender, you can view a detailed breakdown "
                        "Hovering over each region enables you to access with the tooltip to the most "
                        "popular name and the number of individuals who received it on this year or interval "
                        "This tool provides insights into cultural and regional naming preferences over time",
                        p=40,
                        weight=500,
                        size="md",
                    ),
                ],
            ),
        ],
    )
