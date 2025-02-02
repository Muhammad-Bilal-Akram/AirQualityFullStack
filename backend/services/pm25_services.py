from sentinel5plib.analysis import calculate_pm25_indicator, extract_average_data, get_pm_map
from sentinel5plib.vector_utils import convert_geodf_to_dict
from fastapi.responses import JSONResponse
import json
import os

CACHE_DIR = "cache"


def get_air_quality_indicator():

    """
    Retrieve precomputed PM2.5 indicator from cache if available.
    """

    cache_file = f"{CACHE_DIR}/pm25_indicator.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {"message": "Precomputing PM2.5 indicator, try again later."}


def get_pm25_averages():

    """
    Retrieve precomputed PM2.5 averages from cache if available.
    """

    cache_file = f"{CACHE_DIR}/aggregated_pm25.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {"message": "Precomputing PM2.5 averages, try again later."}


def get_pm25_map():

    """
    Retrieve precomputed PM2.5 averages Map from cache if available.
    """

    cache_file = f"{CACHE_DIR}/pm25_map.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    return {"message": "Precomputing PM2.5 Map, try again later."}


def post_air_quality_indicator(request):
    if not request.point_x or not request.point_y:
        return "Please input both latitude and longitude."
    
    df = calculate_pm25_indicator(request.point_x, request.point_y)
    return df if isinstance(df, str) else df.to_dict(orient="records")


def post_pm25_averages(request):
    if not request.year or not request.week_number or not request.month_number:
        return "Please input year, week, and month."
    
    data = extract_average_data(
        point_x=request.point_x, 
        point_y=request.point_y,
        week_number=request.week_number,
        month_number=request.month_number,
        year=request.year
    )
    return data if isinstance(data, str) else data.to_dict(orient="records")


def post_pm25_map(request):
    geojson_data = get_pm_map(
        start_date=request.start_date,
        end_date=request.end_date
    )
    return JSONResponse(content=convert_geodf_to_dict(geojson_data))
