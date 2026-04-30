# backend/schemas.py
#
# Pydantic schemas are the "shape" of data going IN and OUT of your API.
# They are DIFFERENT from SQLAlchemy models, 
#
#   SQLAlchemy Model  = describes a DATABASE TABLE (rows and columns)
#   Pydantic Schema   = describes JSON data for your API (requests and responses)
#
# Why have both? Because you often don't want to expose every database field
# to the outside world (e.g., internal IDs, audit fields). Schemas let you
# control exactly what gets serialized to JSON.

from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- Input Schema (what the API accepts when CREATING a reading) ---
class SensorReadingCreate(BaseModel):
    """
    Used when the robot POSTs a new sensor reading.
    Notice: no `id` or `timestamp` — the database generates those automatically.
    """
    stand_id: str
    temperature: float
    humidity: float


# --- Output Schema (what the API returns when READING data) ---
class SensorReadingOut(BaseModel):
    """
    Used when the API returns sensor data to the frontend.
    Includes id and timestamp because by the time we're reading, DB has set them.
    """
    id: int
    stand_id: str
    temperature: float
    humidity: float
    timestamp: datetime
 
    # `model_config` with `from_attributes=True` tells Pydantic it's allowed to read data directly from a SQLAlchemy model object rather than from a dict.
    model_config = ConfigDict(from_attributes=True)