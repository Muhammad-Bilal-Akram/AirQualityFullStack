from loguru import logger
import ee
from sentinel5plib.data_utils import getPM, calculate_mean


def get_weekly_average_data(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection,
    week_number: int,
    aoi: ee.Geometry
) -> float:

    """
    Calculates the weekly average value for the given week.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :week_number    : Integer
    :aoi            : ee.Geometry

    Output:
    :float
    -----------------------------------------------------------------------------------------
    """

    aai_images = images_aai.filter(ee.Filter.eq('week', week_number))
    aai_image = aai_images.mean()
    no2_images = images_no2.filter(ee.Filter.eq('week', week_number))
    no2_image = no2_images.mean()

    combined = aai_image.addBands(no2_image)
    if combined.bandNames().size().getInfo() == 1:
        return 0
    
    if combined.bandNames().size().getInfo() == 0:
        return 0

    combined = getPM(combined)

    mean_pm25 = calculate_mean(combined, aoi)
    logger.info(f'Week {week_number} average has been extracted')

    return mean_pm25


def get_monthly_average_data(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection,
    month_number: int,
    aoi: ee.Geometry
) -> float:

    """
    Calculates the monthly average value for the given week.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :month_number   : Integer
    :aoi            : ee.Geometry

    Output:
    :float
    -----------------------------------------------------------------------------------------
    """

    aai_images = images_aai.filter(ee.Filter.eq('month', month_number))
    aai_image = aai_images.mean()
    no2_images = images_no2.filter(ee.Filter.eq('month', month_number))
    no2_image = no2_images.mean()

    combined = aai_image.addBands(no2_image)
    if combined.bandNames().size().getInfo() == 1:
        return 0
    
    if combined.bandNames().size().getInfo() == 0:
        return 0

    combined = getPM(combined)

    mean_pm25 = calculate_mean(combined, aoi)
    logger.info(f'Month {month_number} average has been extracted')

    return mean_pm25


def get_yearly_average_data(
    images_aai: ee.ImageCollection,
    images_no2: ee.ImageCollection,
    year: int,
    aoi: ee.Geometry,
) -> float:
    
    """
    Calculates the yearly average value for the given week.
    -----------------------------------------------------------------------------------------
    Required:
    :images_aai     : ee.ImageCollection
    :images_no2     : ee.ImageCollection
    :month_number   : Integer
    :aoi            : ee.Geometry

    Output:
    :float
    -----------------------------------------------------------------------------------------
    """

    aai_image = images_aai.mean()
    no2_image = images_no2.mean()

    combined = aai_image.addBands(no2_image)
    if combined.bandNames().size().getInfo() == 1:
        return 0
    
    if combined.bandNames().size().getInfo() == 0:
        return 0

    combined = getPM(combined)

    mean_pm25 = calculate_mean(combined, aoi)
    logger.info(f'Year {year} average has been extracted')

    return mean_pm25
