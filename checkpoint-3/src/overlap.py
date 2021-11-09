from shapely.geometry import Polygon
import geopandas
import json


def read_file():
    path_to_data1 = geopandas.datasets.get_path("nybb")
    df1 = geopandas.read_file(path_to_data1)
    path_to_data2 = geopandas.datasets.get_path("nybb")
    df2 = geopandas.read_file(path_to_data2)
    return df1, df2


def get_overlap(def1, def2):
    return df1.overlay(df2, how="intersection")


def compare_area(polys_series):
    polys_series["area"] = polys_series.area
    return polys_series["area"].max()

def replace_data(def_final):
