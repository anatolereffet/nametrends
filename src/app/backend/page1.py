from dash import Input, Output
import altair as alt
import pandas as pd
import logging
import warnings
from src.app.backend.utils import FRENCH_DEPARTMENTS

warnings.filterwarnings(
    "ignore",
    "Geometry is in a geographic CRS. Results from 'centroid' are likely incorrect.",
)


# TODO: Setup global logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_empty_departments(
    table: pd.DataFrame, departments_polygons: pd.DataFrame, year: int, sex: int
) -> pd.DataFrame:
    """
    Add the missing departments with the corresponding polygons.
    This is a hardcoded function for the year and sex
    will be fixed later
    Args:
        table (pd.DataFrame): filtered table
        departments_polygons (pd.DataFrame): dataframe holding code, name and shape of the departments
    Returns:
        pd.DataFrame: full table with missing polygons
    """
    missing_dpts = sorted(
        [str(dpt) for dpt in FRENCH_DEPARTMENTS if dpt not in table.dpt.unique()]
    )
    missing_polygons = departments_polygons[
        departments_polygons["code"].isin(missing_dpts)
    ].set_index("code")

    mia_dpts = {
        "code": missing_dpts,
        "nom": missing_polygons.loc[missing_dpts, "nom"].values,
        "geometry": missing_polygons.loc[missing_dpts, "geometry"].values,
        "sexe": [sex] * len(missing_dpts),
        "prenoms": ["N/A"] * len(missing_dpts),
        "annee": [year] * len(missing_dpts),
        "dpt": missing_dpts,
        "nombre": [0] * len(missing_dpts),
    }

    df = pd.concat([table, pd.DataFrame(mia_dpts)]).reset_index()
    return df


def firstpage_callbacks(app):
    @app.callback(
        [
            Output("graph-altair", "spec"),
        ],
        [Input("slider-altair-map", "value"), Input("gender-control", "value")],
    )
    def update_altair_map(slider_year, selected_gender="male"):
        # Log callback activation
        logger.info("Callback triggered for first page")
        logger.info(f"Chosen year: {slider_year}")
        logger.info(f"Selected gender: {selected_gender}")

        # Ensure 'annee' is treated as an integer
        app.dpd_table["annee"] = app.dpd_table["annee"].astype(int)

        # Select data for specific gender & year
        gender = 1 if selected_gender == "male" else 2
        filtered_data = app.dpd_table[
            (app.dpd_table["annee"] == slider_year) & (app.dpd_table["sexe"] == gender)
        ]

        filtered_data = add_empty_departments(
            filtered_data, app.departments, slider_year, gender
        )

        # Find most common name in each dopt
        most_common_in_dpt = filtered_data.loc[
            filtered_data.groupby("dpt")["nombre"].idxmax()
        ]

        # Calc centroid coordinates for plotting
        most_common_in_dpt["long"] = most_common_in_dpt.geometry.centroid.x
        most_common_in_dpt["lat"] = most_common_in_dpt.geometry.centroid.y

        # IDF Specific processing
        IDF = ["75", "77", "78", "91", "92", "93", "94", "95"]
        idf_only = most_common_in_dpt[most_common_in_dpt["dpt"].isin(IDF)]

        # Find most common names in idf
        if not idf_only.empty:
            most_common_name_idf = idf_only.groupby("prenoms")["nombre"].sum().idxmax()
            most_common_idf = idf_only[idf_only["prenoms"] == most_common_name_idf]

            # Copy & update regions DF
            regions_copy = app.regions.copy()
            regions_copy["prenoms"] = most_common_name_idf
            regions_copy["nombre"] = most_common_idf["nombre"].sum()
            regions_copy["sexe"] = most_common_idf["sexe"].mode().iloc[0]
            regions_copy["long"] = regions_copy.geometry.centroid.x
            regions_copy["lat"] = regions_copy.geometry.centroid.y
            regions_copy["dpt"] = "IDF"

            # Combine non-IDF & IDF data
            combined_data = pd.concat(
                [most_common_in_dpt[~most_common_in_dpt["dpt"].isin(IDF)], regions_copy]
            )
        else:
            combined_data = most_common_in_dpt

        tmp_legend = (
            combined_data.groupby("prenoms", as_index=False)
            .agg({"nombre": "sum"})
            .sort_values(by="nombre", ascending=False)
            .prenoms.values
        )

        # Handle pre-1961 departments that didn't exist
        sorting_order = (
            tmp_legend + ["N/A"] if "N/A" in idf_only.prenoms.values else tmp_legend
        )
        # Create selection for interactive filtering
        selection = alt.selection_point()

        # Color Encoding Definition
        color_encoding = alt.condition(
            selection,
            alt.Color(
                "prenoms:N",
                scale=alt.Scale(scheme="accent"),
                sort=sorting_order,
            ),
            alt.value("lightgray"),
        )

        # Main Map with IDF
        main_map = (
            alt.Chart(combined_data)
            .mark_geoshape(stroke="black")
            .encode(
                tooltip=[
                    alt.Tooltip("prenoms:N"),
                    alt.Tooltip("dpt:N"),
                    alt.Tooltip("nombre:Q"),
                ],  # Explicitly set data types
                color=color_encoding,
            )
            .properties(width=666, height=500)
            .add_params(selection)
        )

        # IDF Separate map
        if not idf_only.empty:
            idf_map = (
                alt.Chart(idf_only)
                .mark_geoshape(stroke="black")
                .encode(
                    tooltip=[
                        alt.Tooltip("prenoms:N"),
                        alt.Tooltip("dpt:N"),
                        alt.Tooltip("nombre:Q"),
                    ],
                    # Explicitly set data types
                    color=color_encoding,
                    text=alt.Text("prenoms:N"),  # Explicitly set as nominal
                )
                .properties(width=333, height=250)
                .add_params(selection)
            )

            # Combining maps
            spacer = (
                alt.Chart()
                .mark_text()
                .encode(text=alt.value(""))
                .properties(height=125)
            )
            final_map = alt.concat(main_map, alt.vconcat(spacer, idf_map, spacer))
        else:
            final_map = main_map

        return [final_map.to_dict()]
