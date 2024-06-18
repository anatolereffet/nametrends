from dash import html, dcc


def create_layout(app):
    unique_names = sorted(app.df.prenoms.unique())
    year_unique = sorted(app.df.annee.unique())

    layout = html.Div(
        [
            html.H1("Global Overview"),
            html.P("We can filter here for a given name and year."),
            dcc.Dropdown(
                id="dropdown-names",
                options=unique_names,
                value=unique_names[0],
                placeholder="Select Name",
            ),
            dcc.Dropdown(
                id="dropdown-year",
                options=year_unique,
                value=year_unique[0],
                placeholder="Select year of interest",
            ),
            html.Div(
                children=[
                    dcc.Graph(
                        id="graph",
                        className="graph-side-by-side",
                    ),
                    dcc.Graph(
                        id="chartyear",
                        className="graph-side-by-side",
                    ),
                ]
            ),
            html.Div(id="table-container"),
        ]
    )
    return layout
