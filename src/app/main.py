import dash
import dash_bootstrap_components as dbc
from backend.callbacks import register_callbacks
from frontend.layout import serve_layout
from src.app.backend.load_data import load_map, load_babynames
import geopandas as gpd

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.title = "French Name Trends"

# Load data in cache
app.df = load_babynames()
app.geojson = load_map()
departments = gpd.read_file("./data/departement_avec_outremer_rapprochee.geojson")
app.regions = gpd.read_file("./data/idf.geojson")
app.dpd_table = departments.merge(app.df, how="right", left_on="code", right_on="dpt")
# Load initial layout
app.layout = lambda: serve_layout(app)

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
