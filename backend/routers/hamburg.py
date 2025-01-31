from fastapi import APIRouter
from fastapi.responses import JSONResponse
from utils_f.geojson_loader import load_hamburg_geojson

router = APIRouter()

@router.get("/map-data")
async def get_hamburg_map_data():
    return JSONResponse(content=load_hamburg_geojson())
