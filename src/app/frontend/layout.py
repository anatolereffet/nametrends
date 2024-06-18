from dash import html, dcc
from .sidebar import sidebar
from .content import content


def serve_layout(app):
    return html.Div([dcc.Location(id="url", refresh=False), sidebar, content])
