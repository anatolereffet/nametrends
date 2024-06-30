from dash import html, dcc
import dash_mantine_components as dmc


def create_layout(app):
    return html.Div(
        children=[
            dmc.Paper(
                className="graph-standalone",
                shadow="sm",
                children=[
                    dmc.Center(
                        style={"height": "100%", "width": "100%"},
                        children=[
                            dcc.Graph(
                                id="sunburst-plot",
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
                                "Select a year",
                                p=40,
                                weight=700,
                                italic=True,
                                size="xl",
                            ),
                        ],
                    ),
                    dmc.Slider(
                        id="slider-sunburst",
                        value=1900,
                        min=1900,
                        max=2020,
                        step=1,
                        labelAlwaysOn=True,
                        updatemode="mouseup",
                        classNames={"label": "custom-tooltip"},
                    ),
                ],
            ),
            dmc.Paper(
                className="text-explanation",
                shadow="xl",
                children=[
                    dmc.Center(
                        children=[
                            dmc.Title("Gender & Religion", order=1),
                        ]
                    ),
                    dmc.Text(
                        "This sunburst chart visualization explores gender effects "
                        "on name popularity over time. Names are categorized by gender "
                        "in the first layer, then divided into Christian and non-Christian "
                        "groups, we then are able to display the top 5 names given in each group",
                        p=40,
                        weight=500,
                        size="md",
                    ),
                    dmc.Text(
                        "The distinction between Christian and non-Christian names highlights "
                        "the influence on religion on naming conventions, particularly noting"
                        "the prominence of Christian names in the early 20th century.",
                        p=40,
                        weight=500,
                        size="md",
                    ),
                ],
            ),
        ],
    )
