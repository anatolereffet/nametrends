import dash
import geopandas as gpd
import dash_bootstrap_components as dbc
import os

from backend.callbacks import register_callbacks
from frontend.layout import serve_layout
from backend.load_data import load_map, load_babynames
from backend.utils import precompute_data


def create_app():
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True,
    )
    app.title = "French Name Trends"

    # Cross-platform paths
    departments_path = os.path.join("data", "departement_avec_outremer_rapprochee.geojson")
    regions_path = os.path.join("data", "idf.geojson")

    # Load data in cache
    app.df = load_babynames()
    app.geojson = load_map()
    departments = gpd.read_file(departments_path)
    app.regions = gpd.read_file(regions_path)
    app.dpd_table = departments.merge(app.df, how="right", left_on="code", right_on="dpt")

    # Load initial layout
    app.layout = lambda: serve_layout(app)

    register_callbacks(app)

    return app


# Create app instance
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
