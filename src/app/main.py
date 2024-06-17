import dash
import dash_bootstrap_components as dbc
from backend.callbacks import create_callbacks
from frontend.layout import layout

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "French Name Trends"

app.layout = layout

create_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
