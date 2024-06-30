import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_mantine_components as dmc


def page_link(pageHref):
    href = f"/{pageHref}"
    style = {}

    emoji = {"homepage": "1️⃣", "regionaleffect": "2️⃣", "sunburst": "3️⃣"}

    return dcc.Link(
        href=href,
        children=[
            dmc.ActionIcon(
                id={"type": "pages-links", "index": pageHref},
                n_clicks=0,
                style=style,
                children=[emoji.get(pageHref)],
            )
        ],
    )


_pages = ["homepage", "regionaleffect", "sunburst"]

sidebar = html.Div(
    className="centered_navbar",
    children=[page_link(p) for p in _pages],
)
