from loguru import logger
import pandas as pd
import ee
from sentinel5plib.data_utils import getPM, calculate_mean
ee.Initialize()


def get_current_day_average(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection, 
    current_day: int, 
    aoi: ee.Geometry
) -> pd.DataFrame:
    
    """
    Calculates the average value for the given day.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :current_day    : Integer
    :aoi            : ee.Geometry

    Output:
    :dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """

    current_daily_aai_images = images_aai.filter(ee.Filter.eq('day', current_day))
    current_daily_aai_image = current_daily_aai_images.mean()
    current_daily_no2_images = images_no2.filter(ee.Filter.eq('day', current_day))
    current_daily_no2_image = current_daily_no2_images.mean()

    combined = current_daily_aai_image.addBands(current_daily_no2_image)

    results = []

    if combined.bandNames().size().getInfo() == 0:
        results.append({'Current_day_week_year': current_day, 'Average_PM2.5': 0})
    
    elif combined.bandNames().size().getInfo() == 1:
        results.append({'Current_day_week_year': current_day, 'Average_PM2.5': 0})

    else:
        combined = getPM(combined)
        mean_pm25 = calculate_mean(combined, aoi)
        results.append({'Current_day_week_year': current_day, 'Average_PM2.5': mean_pm25})

    df = pd.DataFrame(results)
    logger.info(f'Mean values for current day: {current_day} have been extracted')

    return df


def get_current_weekly_average(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection, 
    current_week: int, 
    aoi: ee.Geometry
):
    
    """
    Calculates the average value for the given week.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :current_week   : Integer
    :aoi            : ee.Geometry

    Output:
    :dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """
    
    current_week_aai_images = images_aai.filter(ee.Filter.eq('week', current_week))
    current_week_aai_image = current_week_aai_images.mean()
    current_week_no2_images = images_no2.filter(ee.Filter.eq('week', current_week))
    current_week_no2_image = current_week_no2_images.mean()

    combined = current_week_aai_image.addBands(current_week_no2_image)

    results = []

    if combined.bandNames().size().getInfo() == 0:
        results.append({'Current_day_week_year': current_week, 'Average_PM2.5': 0})

    elif combined.bandNames().size().getInfo() == 1:
        results.append({'Current_day_week_year': current_week, 'Average_PM2.5': 0})

    else:
        combined = getPM(combined)
        mean_pm25 = calculate_mean(combined, aoi)
        results.append({'Current_day_week_year': current_week, 'Average_PM2.5': mean_pm25})

    df = pd.DataFrame(results)
    logger.info(f'Mean values for current week: {current_week} have been extracted')

    return df


def get_current_year_average(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection, 
    current_year: int, 
    aoi: ee.Geometry
):

    """
    Calculates the average value for the given week.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :current_year   : Integer
    :aoi            : ee.Geometry

    Output:
    :dataframe      : pd.DataFrame
    -----------------------------------------------------------------------------------------
    """
    
    current_year_aai_image = images_aai.mean()
    current_year_no2_image = images_no2.mean()

    combined = current_year_aai_image.addBands(current_year_no2_image)

    results = []

    if combined.bandNames().size().getInfo() == 0:
        results.append({'Current_day_week_year': current_year, 'Average_PM2.5': 0})

    elif combined.bandNames().size().getInfo() == 1:
        results.append({'Current_day_week_year': current_year, 'Average_PM2.5': 0})

    else:
        combined = getPM(combined)
        mean_pm25 = calculate_mean(combined, aoi)
        results.append({'Current_day_week_year': current_year, 'Average_PM2.5': mean_pm25})

    df = pd.DataFrame(results)
    logger.info(f'Mean values for current year: {current_year} have been extracted')

    return df