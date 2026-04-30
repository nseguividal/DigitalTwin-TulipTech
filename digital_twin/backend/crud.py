# backend/crud.py
#
# CRUD = Create, Read, Update, Delete.
# This file contains all direct database interaction logic.
# Your API routes call these functions — they don't touch the DB directly.

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
 
import models
import schemas

# --- CREATE ---
async def create_sensor_reading(
    db: AsyncSession, reading: schemas.SensorReadingCreate
) -> models.SensorReading:
    """
    Inserts a new SensorReading row into the database.
    """
    # Create a new SQLAlchemy model instance from the Pydantic schema data.
    # GETS: {"stand_id": "A1", "temperature": 21.4, "humidity": 68.5}
    # GIVES: models.SensorReading(stand_id="A1", temperature=21.4, humidity=68.5)
    db_reading = models.SensorReading(**reading.model_dump())

    # Stage the new object, it's in memory but not yet in the DB.
    db.add(db_reading)

    # Pauses while the DB does its work. And refreshes it, updating db_reading with the values the database generated. Once the DB responds, execution resumes here.
    await db.commit()
    await db.refresh(db_reading)

    return db_reading

# --- READ ---
async def get_sensor_readings(
    db: AsyncSession,
    stand_id: str | None = None,
    limit: int = 100,
) -> list[models.SensorReading]:
    """
    Fetches sensor readings from the database, optionally filtered by stand_id.
    Returns a list of SensorReading objects.
    """
    query = select(models.SensorReading)

    # Conditionally add a WHERE clause only if stand_id was provided.
    if stand_id:
        query = query.where(models.SensorReading.stand_id == stand_id)
    
    # Order by newest first, and cap the results to avoid giant payloads.
    query = query.order_by(desc(models.SensorReading.timestamp)).limit(limit)
    
    # `execute` sends the query to the DB. `await` yields control until it responds.
    result = await db.execute(query)

    # `scalars().all()` extracts the list of SensorReading objects from the result.
    return result.scalars().all()


