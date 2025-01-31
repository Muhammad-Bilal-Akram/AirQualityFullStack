import json
import os
from loguru import logger
from sentinel5plib.analysis import (
    calculate_pm25_indicator,
    extract_average_data,
    get_pm_map
)
from sentinel5plib.vector_utils import convert_geodf_to_dict

CACHE_DIR = "cache"
INDICATOR_CACHE_FILE = f"{CACHE_DIR}/pm25_indicator.json"
AVERAGES_CACHE_FILE = f"{CACHE_DIR}/aggregated_pm25.json"
MAP_CACHE_FILE = f"{CACHE_DIR}/pm25_map.json"


def precompute_metrics():

    """
    Precomputes and caches PM2.5 indicator, averages, and map data.
    """
    
    os.makedirs(CACHE_DIR, exist_ok=True)

    try:
        logger.info('Precomputing and Caching PM2.5 Indicator')
        indicator_data = calculate_pm25_indicator().to_dict(orient="records")
        with open(INDICATOR_CACHE_FILE, "w") as f:
            json.dump(indicator_data, f)
        logger.success('PM2.5 Indicator successfully cached.')

        logger.info('Precomputing and Caching Average PM2.5')
        averages_data = extract_average_data().to_dict(orient="records")
        with open(AVERAGES_CACHE_FILE, "w") as f:
            json.dump(averages_data, f)
        logger.success('PM2.5 average values successfully cached.')

        logger.info('Precomputing and Caching Average PM2.5 Maps')
        geojson_data = get_pm_map()
        geojson_response = convert_geodf_to_dict(geojson_data)
        with open(MAP_CACHE_FILE, "w") as f:
            json.dump(geojson_response, f)
        logger.success('PM2.5 Average Values Map successfully cached.')

    except Exception as e:
        print(f"Precompute failed: {str(e)}")
