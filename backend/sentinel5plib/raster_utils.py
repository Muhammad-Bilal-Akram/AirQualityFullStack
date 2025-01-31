import rasterio
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
from loguru import logger
from sentinel5plib.defaults import (
    DEFAULT_MAP_RASTER_OUTPUT_PATH,
    DEFAULT_MAP_VECTOR_OUTPUT_PATH
)


def raster_to_vector(
    map_raster_file_path: Path = DEFAULT_MAP_RASTER_OUTPUT_PATH, 
    map_vector_file_path: Path = DEFAULT_MAP_VECTOR_OUTPUT_PATH
) -> gpd.GeoDataFrame:

    """
    Converts raster file to vector file.
    -----------------------------------------------------------------------------------------
    Required:
    :map_raster_file_path   : Path to raster file
    :map_vector_file_path   : Path to vector file

    Output:
    :GeoDataFrame           : gpd.GeoDataFrame
    -----------------------------------------------------------------------------------------
    """

    with rasterio.open(map_raster_file_path) as src:

        image = src.read(1)
        transform = src.transform
        height, width = image.shape

        points = []
        values = []

        for row in range(height):
            for col in range(width):
                value = image[row, col]
                if value != src.nodata:
                    x, y = transform * (col, row)
                    point = Point(x, y)
                    points.append(point)
                    values.append(value)

        gdf = gpd.GeoDataFrame({'PM2.5': values}, geometry=points)
        gdf.to_file(map_vector_file_path, driver='GeoJSON')

        logger.info('Raster file has been converted to vector successfully.')

        return gdf
        
