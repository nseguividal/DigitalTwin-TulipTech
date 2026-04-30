# backend/routers/sensors.py
#
# This file defines the HTTP routes (endpoints) for sensor data.

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

import crud
import schemas
from database import get_db

router = APIRouter(prefix="/api/sensors", tags=["Sensors"])

# --- CREATE ---
@router.post("/", response_model=schemas.SensorReadingOut, status_code=201)
async def create_reading(
    reading: schemas.SensorReadingCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    POST /api/sensors/

    Endpoint to create a new sensor reading.
    Expects JSON body with `stand_id`, `temperature`, and `humidity`.
    Returns the created reading with its assigned `id` and `timestamp`.
    """
    return await crud.create_sensor_reading(db=db, reading=reading)

# --- READ ---
@router.get("/", response_model=list[schemas.SensorReadingOut])
async def get_readings(
    stand_id: str | None = Query(default=None, description="Filter by stand ID"),
    limit: int = Query(default=50, ge=1, le=500, description="Max rows to return"),
    db: AsyncSession = Depends(get_db),
):
    """
    GET /api/sensors/?stand_id=A1&limit=20

    Endpoint to fetch sensor readings.
    Optional query parameters:
    - `stand_id`: filter readings by a specific flower stand
    - `limit`: maximum number of readings to return (default 50, max 500)
    
    Returns a list of sensor readings, ordered by newest first.
    """
    readings = await crud.get_sensor_readings(db=db, stand_id=stand_id, limit=limit)

    if not readings:
        # Return empty list — not a 404, because "no data yet" is valid.
        return []
    
    return readings
 


 

