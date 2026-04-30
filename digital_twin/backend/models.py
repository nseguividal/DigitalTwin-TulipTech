# backend/models.py
#
# This file defines the database TABLES as Python classes.
# Each class = one table. Each class attribute = one column.
# SQLAlchemy translates these into SQL CREATE TABLE statements.

from datetime import datetime
from sqlalchemy import Float, Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base

# Table 1 - The SensorReading Table
class SensorReading(Base):
    """
    Represents a single sensor reading snapshot from the robot.
 
    When the robot scans an AprilTag, it gets temp/humidity for that stand.
    One row in this table = one scan event.
    """
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Which physical flower stand the robot was at when it read this data.
    stand_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    # The actual sensor values.
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)

    # When did the robot take this reading? Defaults to the current time when inserted.
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

# Table 2 - The AnomalyLog Table
class AnomalyLog(Base):
    """
    Represents a detected flower anomaly or disease flag.
 
    When the vision system detects something on a flower, it logs it here.
    This table is a placeholder for now — we'll expand it later.
    """
    __tablename__ = "anomaly_logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Which physical flower stand the robot was at when it read this data.
    stand_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    # Type of anomaly we detect: a short label like "rust_disease", "height_outlier", etc.
    anomaly_type: Mapped[str] = mapped_column(String, nullable=False)

    # OPTIONAL: confidence score from the vision model (0.0 to 1.0)
    confidence: Mapped[float] = mapped_column(Float, nullable=True)

    # When did the robot take this reading? Defaults to the current time when inserted.
    timestamp: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

