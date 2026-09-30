from fastapi import FastAPI, status
from api.db.database import Base, engine

app = FastAPI(title="IncidentOps", description="An API service application for handling incidents and operations.", version="1.0.0")

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "message": "Hello World!"
    }