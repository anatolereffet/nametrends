import pandas as pd
import plotly.express as px
from app.backend.utils import add_missing_departments


def map(babynames: pd.DataFrame, departements: pd.DataFrame, prenom: str, annee: str) -> None:
    """Displays a heat map of French departments comparing the number of babies of the same name born in the same year

    Args:
        babynames (pd.DataFrame): Names given at birth by date, sex and department of birth
        departements (pd.DataFrame): Names, numbers and contact details of French departments
        prenom (str): First name to be searched
        annee (str): Year to be searched
    """
    prenom = prenom.upper()
    year_filter = babynames.loc[babynames['annee']== annee]
    name_filter = year_filter.loc[year_filter['prenoms'] == prenom]
    data = add_missing_departments(name_filter)

    fig = px.choropleth(data_frame=data, geojson=departements,
                        locations='dpt', color='nombre',
                        featureidkey='properties.code',
                        projection="mercator")

    fig.update_geos(fitbounds="geojson", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},  dragmode=False)
    fig.show()