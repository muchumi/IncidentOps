from fastapi import FastAPI, status
from api.db.database import Base, engine
from api.views import user, task

app = FastAPI(title="IncidentOps", description="An API service application for handling incidents and operations.", version="1.0.0")

# Registering routers using app.include_router()
app.include_router(user.router)

# create tables
Base.metadata.create_all(bind=engine)

# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
def read_root():
    return {
        "message": "Hello World!"
    }