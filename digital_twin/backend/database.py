# backend/database.py
#
# This file is responsible for ONE thing: setting up the connection to SQLite.

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# --- The Database URL ---
# SQLAlchemy uses SQLite with async-compatible driver (aiosqlite)
DATABASE_URL = "sqlite+aiosqlite:///./greenhouse.db"

# --- The Engine ---
# The persistent connection to the DB. Lives for the app's lifetime.
# echo=True is an aid: it prints every SQL statement SQLAlchemy sends to the database into the terminal. 
# -!!- SET TO FALSE before deploying, its only for debugging!!!!
engine = create_async_engine(DATABASE_URL, echo=True)

# --- The Session Factory ---
# A factory that stamps out fresh sessions on demand.
# A session is a temporary workspace, where we add things (queries, inserts), and then "commit" to save them all at once.
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --- The Base ---
# The Base is the shared parent class that all the database table definitions will inherit from.
class Base(DeclarativeBase):
    pass


# --- The Dependency ---
# FastAPI dependency, opens a session, hands it to a route, closes it after.
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


# FastAPI pattern to get info, use it, and clean it up.
#1. FastAPI calls get_db()
#2. get_db() creates a fresh session  ← AsyncSessionLocal()
#3. get_db() yields the session to the route function
#4. The route function runs, uses the session, returns a response
#5. get_db() resumes after yield
#6. `async with` block exits → session is automatically closed





