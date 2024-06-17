from dash import html, dcc
from .sidebar import sidebar
from .content import content

layout = html.Div([dcc.Location(id="url"), sidebar, content])
