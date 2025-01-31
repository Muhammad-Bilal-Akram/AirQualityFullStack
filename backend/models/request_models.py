from typing import Optional
from pydantic import BaseModel
from sentinel5plib.defaults import (
    DEFAULT_AVERAGE_WEEK_VALUE,
    DEFAULT_AVERAGE_MONTH_VALUE,
    DEFAULT_AVERAGE_YEAR_VALUE,
    DEFAULT_MAP_DATA_START_DATE,
    DEFAULT_MAP_DATA_END_DATE
)


class CurrentPointRequest(BaseModel):
    point_x: Optional[float] = None
    point_y: Optional[float] = None


class AveragePointRequest(BaseModel):
    point_x: Optional[float] = None
    point_y: Optional[float] = None
    week_number: Optional[int] = DEFAULT_AVERAGE_WEEK_VALUE
    month_number: Optional[int] = DEFAULT_AVERAGE_MONTH_VALUE
    year: Optional[int] = DEFAULT_AVERAGE_YEAR_VALUE


class MapRequest(BaseModel):
    start_date: Optional[str] = DEFAULT_MAP_DATA_START_DATE
    end_date: Optional[str] = DEFAULT_MAP_DATA_END_DATE
    
