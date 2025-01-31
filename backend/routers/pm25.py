from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
import json
import os
from models.request_models import CurrentPointRequest, AveragePointRequest, MapRequest
from services.pm25_services import (
    post_air_quality_indicator,
    post_pm25_averages,
    post_pm25_map,
)
from utils_f.cache import precompute_metrics

router = APIRouter()
CACHE_DIR = "cache"


@router.get("/indicator")
async def air_quality_indicator():
    cache_file = f"{CACHE_DIR}/pm25_indicator.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)

    precompute_metrics()
    return {"message": "Precomputing PM2.5 indicator, try again later."}


@router.get("/averages")
async def pm25_averages():
    cache_file = f"{CACHE_DIR}/aggregated_pm25.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)

    precompute_metrics()
    return {"message": "Precomputing PM2.5 averages, try again later."}


@router.get("/map-data")
async def pm25_map():
    cache_file = f"{CACHE_DIR}/pm25_map.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)

    precompute_metrics()
    return {"message": "Precomputing PM2.5 map, try again later."}


@router.post("/recompute")
async def recompute_pm25():
    precompute_metrics()
    return {"message": "PM2.5 data recomputed successfully"}


@router.post("/indicator")
async def post_air_quality(request: CurrentPointRequest):
    try:
        return post_air_quality_indicator(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/averages")
async def post_pm25_avg(request: AveragePointRequest):
    try:
        return post_pm25_averages(request)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/map-data")
async def post_pm25_map_data(request: MapRequest):
    try:
        return post_pm25_map(request)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
