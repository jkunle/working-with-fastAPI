from fastapi import FastAPI, HTTPException, Depends
from schemas import load_db, save_db, CarInput, CarOutput, TripInput, TripOutput, Car
from sqlmodel import SQLModel, select
from db import engine
from routers import cars
from datetime import datetime


app = FastAPI(title="Car Sharing")
app.include_router(cars.router)

db = load_db()


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
    

        
if __name__ == "__main__":
    uvicorn.run("carsharing:app", reload=True)