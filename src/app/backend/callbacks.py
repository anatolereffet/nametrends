from dash import Output, Input, html

from src.app.frontend.pages import homepage, page1
from src.app.backend.homepage import home_callbacks


def register_layout_callback(app):
    @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
    def render_page_content(pathname):
        if pathname == "/" or pathname == "/homepage":
            return homepage.create_layout(app)
        elif pathname == "/page-1":
            return page1.layout
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

    # Layout specific callbacks
    register_layout_callback(app)
