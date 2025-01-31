from loguru import logger
from pathlib import Path
from typing import Optional
import datetime
import numpy as np
import pandas as pd
import geopandas as gpd
import ee
import geemap
from sentinel5plib.vector_utils import vector_to_ee_geometry_object
from sentinel5plib.raster_utils import raster_to_vector

from sentinel5plib.current_avg_utils import (
    get_current_day_average,
    get_current_weekly_average,
    get_current_year_average
)

from sentinel5plib.avg_utils import (
    get_weekly_average_data,
    get_monthly_average_data,
    get_yearly_average_data
)

from sentinel5plib.data_utils import (
    get_sentinel5p_image_collection, 
    convertNO2MolM2ToMicrogramM3,
    getPM,
    get_sentinel5p_image_collection_range
)

from sentinel5plib.defaults import (
    HAMBURG_GEOJSON_PATH,
    DEFAULT_AVERAGE_WEEK_VALUE,
    DEFAULT_AVERAGE_MONTH_VALUE,
    DEFAULT_AVERAGE_YEAR_VALUE,
    DEFAULT_MAP_RASTER_OUTPUT_PATH,
    DEFAULT_MAP_DATA_START_DATE,
    DEFAULT_MAP_DATA_END_DATE
)

ee.Initialize()


def extract_average_data(
    point_x: Optional[float] = None, 
    point_y: Optional[float] = None,
    hamburg_geojson_path: Path = HAMBURG_GEOJSON_PATH,
    week_number: Optional[int] = DEFAULT_AVERAGE_WEEK_VALUE,
    month_number: Optional[int] = DEFAULT_AVERAGE_MONTH_VALUE,
    year: Optional[int] = DEFAULT_AVERAGE_YEAR_VALUE, 
) -> pd.DataFrame:

    """
    Calculates PM2.5 average values of a day, week, and month PM25 using NO2_in_µg_per_m3 and 
    absorbing_aerosol_index Bands.
    -----------------------------------------------------------------------------------------
    Default:
    :aoi            : Path

    Optional:
    :point_x        : float
    :point_y        : float
    :year           : Int = 2025
    :week_number    : Int = 1
    :month_number   : Int = 1

    Output:
    :Dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """
    
    if not isinstance(year, int):
        raise ValueError("Year is required and must be an integer.")
    
    if week_number is not None:
        if week_number < 1 or week_number > 53:
            raise ValueError("Week number must be between 1 and 53.")
    
    if month_number is not None:
        if month_number < 1 or month_number > 12:
            raise ValueError("Month number must be between 1 and 12.")
    
    hamburg_aoi = vector_to_ee_geometry_object(hamburg_geojson_path)

    if point_x and point_y:
        point_aoi = ee.Geometry.Point([point_x, point_y])
        intersects = hamburg_aoi.contains(point_aoi)
        if intersects.getInfo():
            aoi = point_aoi
        else:
            return 'Points are out of Hamburg bounding box'
    else:
        aoi = hamburg_aoi

    Images_AAI = get_sentinel5p_image_collection("OFFL", "AER_AI", year, aoi)
    Images_no2 = get_sentinel5p_image_collection("OFFL", "NO2", year, aoi)
    Images_no2 = Images_no2.map(convertNO2MolM2ToMicrogramM3)
    Images_no2 = Images_no2.select('NO2_in_µg_per_m3')

    week_mean_pm25 = get_weekly_average_data(Images_AAI, Images_no2, week_number, aoi)
    month_mean_pm25 = get_monthly_average_data(Images_AAI, Images_no2, month_number, aoi)
    year_mean_pm25 = get_yearly_average_data(Images_AAI, Images_no2, year, aoi)

    df = pd.DataFrame()
    df['Average_week_month_year'] = [week_number, month_number, year]
    df['Average_PM2'] = [week_mean_pm25, month_mean_pm25, year_mean_pm25]
    logger.info('PM2.5 Quality Average Values extracted successfully.')

    return df


def calculate_pm25_indicator(
    point_x: Optional[float] = None, 
    point_y: Optional[float] = None,
    hamburg_geojson_path: str = HAMBURG_GEOJSON_PATH
) -> pd.DataFrame:

    """
    Calculates Current PM2.5 average values of a day, week, and month PM25 using 
    NO2_in_µg_per_m3 and absorbing_aerosol_index Bands.
    -----------------------------------------------------------------------------------------
    Optional:
    :point_x        : float
    :point_y        : float

    Output:
    :Dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """

    current_date = datetime.datetime.now()
    current_year, current_week, current_weekday = current_date.isocalendar()
    current_day = current_date.day

    day_list = [1, 2]
    week_list = [2]

    if current_day not in day_list:
        current_day = current_day - 2

    if current_weekday in week_list:
        current_week = current_week - 1

    hamburg_aoi = vector_to_ee_geometry_object(hamburg_geojson_path)

    if point_x and point_y:
        point_aoi = ee.Geometry.Point([point_x, point_y])
        intersects = hamburg_aoi.contains(point_aoi)
        if intersects.getInfo():
            aoi = point_aoi
        else:
            return 'Points are out of Hamburg bounding box'
    else:
        aoi = hamburg_aoi

    Images_AAI = get_sentinel5p_image_collection("NRTI", "AER_AI", current_year, aoi)
    Images_no2 = get_sentinel5p_image_collection("NRTI", "NO2", current_year, aoi)
    Images_no2 = Images_no2.map(convertNO2MolM2ToMicrogramM3)
    Images_no2 = Images_no2.select('NO2_in_µg_per_m3')

    current_day_mean_pm25 = get_current_day_average(Images_AAI, Images_no2, current_day, aoi)
    current_week_mean_pm25 = get_current_weekly_average(Images_AAI, Images_no2, current_week, aoi)
    current_year_mean_pm25 = get_current_year_average(Images_AAI, Images_no2, current_year, aoi)

    df = pd.concat([current_day_mean_pm25, current_week_mean_pm25, current_year_mean_pm25], axis=0)
    df = df.replace(np.nan, 0)

    aai_day = df['Average_PM2.5'].values[0]
    aai_week = df['Average_PM2.5'].values[1]
    aai_year = df['Average_PM2.5'].values[2]

    if aai_day < 0:
        aai_day = 0

    if aai_week < 0:
        aai_week = 0

    if aai_year != str:
        if aai_day != str:
            aai_day = (aai_day / aai_year) * 100
        else:
            aai_day = aai_day 
        if aai_week != str:
            aai_week = (aai_week / aai_year) * 100
        else:
            aai_week = aai_week 
    else:
        aai_day = aai_day
        aai_week = aai_week

    df['Air_quality_indicator_yearly_comparison'] = [aai_day, aai_week, 0]
    logger.info('PM2.5 Quality Current Values extracted successfully.')

    return df


def get_pm_map(
    hamburg_geojson_path: Path = HAMBURG_GEOJSON_PATH,
    start_date: str = DEFAULT_MAP_DATA_START_DATE,
    end_date: str = DEFAULT_MAP_DATA_END_DATE,
    output_file_path: Path = DEFAULT_MAP_RASTER_OUTPUT_PATH
) -> gpd.GeoDataFrame:
    
    """
    Calculates PM2.5 average values of a time frame, saves it to raster format, and converts
    it to vector format.
    -----------------------------------------------------------------------------------------
    Default:
    :hamburg_geojson_path           : Input path of the hamburg vector file
    :start_date                     : 2025-01-01
    :end_date                       : 2025-12-31
    :output_file_path               : Output path to the raster map

    Output:
    :Dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """

    aoi = vector_to_ee_geometry_object(hamburg_geojson_path)

    Images_AAI = get_sentinel5p_image_collection_range("AER_AI", aoi, start_date, end_date)
    Images_no2 = get_sentinel5p_image_collection_range("NO2", aoi, start_date, end_date)
    Images_no2 = Images_no2.map(convertNO2MolM2ToMicrogramM3)
    Images_no2 = Images_no2.select('NO2_in_µg_per_m3')

    aai_image = Images_AAI.mean()
    no2_image = Images_no2.mean()

    combined = aai_image.addBands(no2_image)
    combined = getPM(combined)

    pm25 = combined.select('PM25').clip(aoi)

    geemap.ee_export_image(pm25, filename=output_file_path, scale=1113.2, region=aoi, file_per_band=False)

    vector_data = raster_to_vector()
    logger.info('Raster data converted to vector data successfully.')
    
    return vector_data
