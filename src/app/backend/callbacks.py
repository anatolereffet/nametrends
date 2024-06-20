from dash import Output, Input, html

from frontend.pages import homepage, page1, barchartrace
from backend.homepage import home_callbacks
from backend.page1 import firstpage_callbacks
from backend.barchartrace import bar_chart_race_callbacks


def register_layout_callback(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/" or pathname == "/homepage":
            return homepage.create_layout(app)
        elif pathname == "/page-1":
            return page1.create_layout(app)
        elif pathname == "/barchartrace":
            return barchartrace.create_layout(app)
        # If the user tries to reach a different page, return a 404 message
        return html.Div(
            [
                html.H1("404: Not found", className="text-danger"),
                html.Hr(),
                html.P(f"The pathname {pathname} was not recognised..."),
            ],
            className="p-3 bg-light rounded-3",
        )


def register_callbacks(app):
    # Page specific callbacks
    home_callbacks(app)
    firstpage_callbacks(app)
    bar_chart_race_callbacks(app)
    # Layout specific callbacks
    register_layout_callback(app)
