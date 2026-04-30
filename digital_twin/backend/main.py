# backend/main.py
#
# This is the entry point — it creates the FastAPI app, wires everything together, and is the file we run with `uvicorn`.

import sys
import os

# Backend directory 
sys.path.insert(0, os.path.dirname(__file__))

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
 
from database import engine, Base
from routers import sensors
 

# --- Lifespan: Startup & Shutdown Logic ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Create all tables defined in our models if they don't exist yet.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created/verified.")
    yield

    # SHUTDOWN: Clean up connections.
    await engine.dispose()
    print("Database connections closed.")


# --- App Initialization ---
app = FastAPI(
    title="Tulip Greenhouse Digital Twin API",
    description="Backend for the autonomous greenhouse robot digital twin.",
    version="0.1.0",
    lifespan=lifespan,
)


# --- CORS Middleware ---
# CORS (Cross-Origin Resource Sharing) is a browser security feature.
# When the HTML file tries to call the FastAPI server, the browser blocks it by default. This middleware tells the browser: "yes, it's okay, I allow this."
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Mount Routers ---
# Attaches the sensors router to the main app.
app.include_router(sensors.router)
# ADD MORE ROUTERS AS WE BUILD THEM!!
# app.include_router(anomalies.router)


# --- Frontend Static Files ---
# `frontend/index.html` becomes accessible at http://localhost:8000/
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")


# --- Health Check ---
# A simple endpoint to verify the server is running, to check connectivity.
@app.get("/api/health", tags=["System"])
async def health_check():
    return {"status": "ok", "message": "Greenhouse Digital Twin API is running."}
 
 