from fastapi import FastAPI
from .database import engine, Base
from .routers import patients
from fastapi.middleware.cors import CORSMiddleware


Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "Root",
        "description": "The root endpoint of the API."
    },
    {
        "name": "patients",
        "description": "Operations with patients. Includes creating, reading, updating, and deleting patient records.",
    },
]

app = FastAPI(
    title="Healthcare Dashboard API",
    description="API for managing patient data for the healthcare dashboard.",
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(patients.router)

@app.get("/", tags=["Root"])
def read_root():
    """
    Returns a simple status message to confirm the API is running.
    """
    return {"status": "ok", "message": "Welcome to the Healthcare Dashboard API"}

