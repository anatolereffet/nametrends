from dash import html, dcc
import dash_mantine_components as dmc


def create_layout(app):
    unique_names = sorted(app.df.prenoms.unique())

    layout = html.Div(
        [
            dmc.Paper(
                className="graph-standalone",
                shadow="sm",
                children=[
                    dmc.Center(
                        style={"height": "100%", "width": "100%"},
                        children=[
                            dcc.Graph(
                                id="chartyear",
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
                                "Select a name",
                                p=40,
                                weight=700,
                                italic=True,
                                size="xl",
                            ),
                        ],
                    ),
                    dmc.Center(
                        [
                            dmc.MultiSelect(
                                id="dropdown-names",
                                style={"width": "50%"},
                                clearable=True,
                                value=["JEAN", "DAVID", "ADAM"],
                                data=unique_names,
                                searchable=True,
                                w=200,
                                mb=10,
                            )
                        ]
                    ),
                ],
            ),
            dmc.Paper(
                className="text-explanation",
                shadow="xl",
                children=[
                    dmc.Center(
                        children=[
                            dmc.Title("Time Trends", order=1),
                        ]
                    ),
                    dmc.Text(
                        "The evolution of baby names over time reflects cultural shifts, societal influences, and trends. "
                        "Some names maintain consistent popularity due to their classical appeal, while others "
                        "experience brief surges influenced by pop culture, celebrities or historical events",
                        p=40,
                        weight=500,
                        size="md",
                    ),
                    dmc.Text(
                        "By selecting one or multiple names, you'll see either a histogram (single name) or a line chart. "
                        "The line chart on a y-log scale helps visualizing trends, such as Jean, David and Adam",
                        p=40,
                        weight=500,
                        size="md",
                    ),
                ],
            ),
        ]
    )
    return layout
