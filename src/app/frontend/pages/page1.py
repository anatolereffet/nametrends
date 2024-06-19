from dash import html, dcc
import dash_vega_components as dvc


def create_layout(app):
    unique_names = sorted(app.df.prenoms.unique())
    # year_unique = sorted(app.df.annee.unique())

    layout = html.Div(
        [
            html.H1("Altair Maps"),
            html.P("Replica of homepage but in Altair"),
            dcc.Dropdown(
                id="dropdown-names_altair",
                options=unique_names,
                value=unique_names[0],
                placeholder="Select Name",
            ),
            html.Div(
                dvc.Vega(
                    id="graph-altair",
                    opt={"renderer": "canvas", "actions": False},
                ),
                className="centered_div",
            ),
        ]
    )
    return layout
