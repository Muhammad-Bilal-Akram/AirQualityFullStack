import geopandas as gpd
from functools import reduce
import numpy as np
from pathlib import Path
from loguru import logger
import ee
ee.Initialize()


def vector_to_ee_geometry(input_vector: Path) -> ee.Geometry:

    """
    Converts the vector geometry into ee supported geometry.
    -----------------------------------------------------------------------------------------
    Required:
    :input_vector   : Path to geojson vector file

    Output:
    :Geometry       : ee.Geometry
    -----------------------------------------------------------------------------------------
    """

    gdf = gpd.read_file(input_vector)

    if gdf.geom_type[0] == 'Polygon':
        logger.info(f'{gdf.geom_type[0]} Geometry has been found. '
                    'Extracting the coorindates ...')

        for geom in range(len(gdf)):
            shapely_geometry = [geom for geom in gdf.geometry]
            longitude, latitude = shapely_geometry[geom].exterior.coords.xy
            coordinates = np.dstack((longitude,latitude)).tolist()

            logger.info('Coordinates are successfully extracted. '
                        'Converting it to ee supported Geometry')
            return ee.Geometry.Polygon(coordinates)

    elif gdf.geom_type[0] == 'LineString':
        logger.info(f'{gdf.geom_type[0]} Geometry has been found. '
                    'Extracting the coorindates ...')

        for geom in range(len(gdf)):
            shapely_geometry = [geom for geom in gdf.geometry]
            longitude, latitude = shapely_geometry[geom].exterior.coords.xy
            coordinates = np.dstack((longitude,latitude)).tolist()
            lists = reduce(lambda longitude, latitude: longitude+latitude, coordinates)

            logger.info('Coordinates are successfully extracted and converted to two List. '
                        'Converting it to ee supported Geometry')
            return ee.Geometry.LineString(lists)

    elif gdf.geom_type[0] == 'Point':
        logger.info(f'{gdf.geom_type[0]} Geometry has been found. '
                    'Extracting the coorindates ...')

        for geom in range(len(gdf)):
            shapely_geometry = [geom for geom in gdf.geometry]
            longitude, latitude = shapely_geometry[geom].exterior.coords.xy
            coordinates = np.dstack((longitude,latitude)).tolist()
            lists = reduce(lambda longitude, latitude: longitude+latitude, coordinates)
            point_list = reduce(lambda longitude, latitude: longitude+latitude, lists)

            logger.info('Coordinates are successfully extracted, converted it List of Points . '
                        'Converting it to ee supported Geometry')
            return ee.Geometry.Point(point_list)


def ee_geometry_to_feature(geometry: ee.Geometry) -> ee.Feature:

    """
    Converts the ee Geometry to ee Feature.
    -----------------------------------------------------------------------------------------
    Required:
    :geometry       : ee.Geometry

    Output:
    :geometry       : ee.Features
    -----------------------------------------------------------------------------------------
    """

    logger.info('Converting ee support geometries to features.')
    return ee.Feature(geometry)


def ee_feature_to_featureCollection(feature: ee.Feature) -> ee.FeatureCollection:

    """
    Converts the ee Features to ee Feature Collection.
    -----------------------------------------------------------------------------------------
    Required:
    :geometry       : ee.Features

    Output:
    :geometry       : ee.Features.Collection
    -----------------------------------------------------------------------------------------
    """

    logger.info('Converting and combining ee support features to features collections.')
    return ee.FeatureCollection(feature)


def ee_featureCollection_to_geometry(featurecollection: ee.FeatureCollection) -> ee.Geometry:

    """
    Converts the ee Features to ee Feature Collection.
    -----------------------------------------------------------------------------------------
    Required:
    :geometry       : ee.Features.Collection

    Output:
    :geometry       : ee.Geometry
    -----------------------------------------------------------------------------------------
    """

    logger.info('Extracting ee supported geometries from features collections.')
    return ee.FeatureCollection.geometry(featurecollection) 


def vector_to_ee_geometry_object(input_vector: Path) -> ee.Geometry:

    """
    Read the vector file, converts its geometry to ee supported geometry,
    converts the ee geometry to ee feature, ee features to ee features
    collections, and returns ee geometries from ee feature collections.
    -----------------------------------------------------------------------------------------
    Required:
    :input_vector   : Path to vector file

    Output:
    :geometry       : ee.Geometry
    -----------------------------------------------------------------------------------------
    """

    ee_geometry = vector_to_ee_geometry(input_vector)
    logger.success('EE geometries are successfully extracted.')

    ee_feature = ee_geometry_to_feature(ee_geometry)
    logger.success('EE geometries are successfully converted to features.')

    ee_featurecollection = ee_feature_to_featureCollection(ee_feature)
    logger.success('EE features are successfully converted to feature collections.')

    ee_final_geometries = ee_featureCollection_to_geometry(ee_featurecollection)
    logger.success('EE features collection are successfully converted to geometries.')
    return ee_final_geometries


def convert_geodf_to_dict(geodf_data: gpd.GeoDataFrame) -> dict:

    """
    Converts Geodataframe to dict.
    -----------------------------------------------------------------------------------------
    Required:
    :geodf_data     : gpd.GeoDataFrame

    Output:
    :dict           : Geometeries
    -----------------------------------------------------------------------------------------
    """

    features = []

    for _, row in geodf_data.iterrows():
        point = row['geometry'] 
        longitude, latitude = point.x, point.y 
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude] 
            },
            "properties": {
                "PM2.5": row['PM2.5']
            }
        }
        features.append(feature)

    geojson_response = {
        "type": "FeatureCollection",
        "features": features
    }
    logger.info('Geodataframe has been converted to dict successfully.')

    return geojson_response
