from loguru import logger
import ee
ee.Initialize()


def selectAAI(image: ee.Image) -> ee.Image:

    """
    Selects Absorbed Aerosol Index band from list of bands.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    bands = image.select(['absorbing_aerosol_index'])
    logger.info('Absorbing Aerosol Index band has been selected.')

    return bands


def selectNO2(image: ee.Image) -> ee.Image:

    """
    Selects NO2 Column Number Density band from list of bands.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    bands = image.select(['NO2_column_number_density'])
    logger.info('NO2 Column Number Density band has been selected.')

    return bands


def addDAY_of_year(image: ee.Image) -> ee.Image:
    """
    Adds day number to the properties.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    day = image.date().get('day')
    logger.info('Day numbers added.')
    
    return image.set('day', day)


def addWEEK_of_year(image: ee.Image) -> ee.Image:

    """
    Adds week number to the properties.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    week = image.date().get('week')
    logger.info('Week numbers added.')

    return image.set('week', week)


def addMONTH_of_year(image: ee.Image) -> ee.Image:

    """
    Adds month number to the properties.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    month = image.date().get('month')
    logger.info('Month numbers added.')
    
    return image.set('month', month)


def convertNO2MolM2ToMicrogramM3(
    image: ee.Image,
    atmospheric_height: float = 1000.0,
    molecular_weight_no2: float = 46.0055
) -> ee.Image:
    """
    Converts NO2 data (NO2_column_number_density band) from mol/m² to µg/m³.
    - Atmospheric_height -> assumed to be 1000.0 in meters
    - Molecular weight of NO2 (in grams per mole)
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image 
    -----------------------------------------------------------------------------------------
    """
    
    no2 = image.select('NO2_column_number_density')
    
    # mol/m² to mol/m³
    no2_in_mol_m3 = no2.divide(atmospheric_height)
    
    # mol/m³ to µg/m³ (multiply by molecular weight of NO2 and 1e6 for µg)
    no2_in_microgram_m3 = no2_in_mol_m3.multiply(molecular_weight_no2).multiply(1e6)
    
    image = image.addBands(no2_in_microgram_m3.rename('NO2_in_µg_per_m3'))
    logger.info('NO2_in_µg_per_m3 band has been added to the Image Collection.')
    
    return image


def get_sentinel5p_image_collection(
    product: str,
    data: str, 
    year: int, 
    aoi: ee.Geometry
) -> ee.ImageCollection:
    
    """
    Downloads Sentinel 5P data for given image collection, AOI, and year.
    -----------------------------------------------------------------------------------------
    Required:
    :product    : NRTI/OFFL
    :data       : NO2 or AER_AI
    :year       : Integer
    :aoi        : ee.Geometry

    Output:
    :images     : ee.imageCollection
    -----------------------------------------------------------------------------------------
    """

    if data == 'NO2':
        band_name = 'NO2_column_number_density'
    else:
        band_name = 'absorbing_aerosol_index'
    
    images = ee.ImageCollection(
        f"COPERNICUS/S5P/{product}/L3_{data}"
        ).filterBounds(aoi
        ).filterDate(f"{year}-01-01", f"{year}-12-31"
        ).map(addDAY_of_year
        ).map(addWEEK_of_year
        ).map(addMONTH_of_year
        ).select(band_name)
    logger.info(f'{product}/{data} Images has been extracted.')
    
    return images


def get_sentinel5p_image_collection_range(
    data: str, 
    aoi: ee.Geometry,
    start_date: str,
    end_date: str
) -> ee.ImageCollection:
    
    """
    Downloads Sentinel 5P data for given image collection, AOI, and time-scale.
    -----------------------------------------------------------------------------------------
    Required:
    :data       : NO2 or AER_AI
    :aoi        : ee.Geometry
    :start_date : str
    :end_date   : str

    Output:
    :images     : ee.imageCollection
    -----------------------------------------------------------------------------------------
    """

    if data == 'NO2':
        band_name = 'NO2_column_number_density'
    else:
        band_name = 'absorbing_aerosol_index'
    
    images = ee.ImageCollection(
        f"COPERNICUS/S5P/OFFL/L3_{data}"
        ).filterBounds(aoi
        ).filterDate(f"{start_date}", f"{end_date}"
        ).map(addDAY_of_year
        ).map(addWEEK_of_year
        ).map(addMONTH_of_year
        ).select(band_name)
    logger.info(f'OFFL/{data} Images has been extracted.')
    
    return images


def getPM(image: ee.image) -> ee.image:

    """
    Calculates PM using NO2_in_µg_per_m3 and absorbing_aerosol_index Bands. Adds the PM25
    band in the Image.
    -----------------------------------------------------------------------------------------
    Required:
    :image       : ee.Image

    Output:
    :image       : ee.Image
    -----------------------------------------------------------------------------------------
    """

    PM25 = image.expression(
        '(5 * NO2) + (30 * AAI)', {
            'NO2': image.select('NO2_in_µg_per_m3'),
            'AAI': image.select('absorbing_aerosol_index')
        }).rename("PM25")
    image = image.addBands(PM25)
    logger.info('PM25 band has been added.')

    return(image)


def calculate_mean(image: ee.Image, aoi: ee.Geometry) -> float:

    """
    Calculates mean of an image for the given geometry.
    -----------------------------------------------------------------------------------------
    Required:
    :image      : ee.Image
    :aoi        : ee.Geometry

    Output:
    :Average    : Float
    -----------------------------------------------------------------------------------------
    """

    mean_aai = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=aoi,
        scale=1113.2, 
        maxPixels=1e8
    ).get('PM25').getInfo()
    logger.info('Average value has been calculated.')

    return mean_aai