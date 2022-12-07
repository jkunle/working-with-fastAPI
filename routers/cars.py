from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from schemas import Car, CarOutput, CarInput, TripInput, TripOutput


router = APIRouter()

@router.get("/api/cars")
def get_cars(size: str|None = None, doors: int|None = None, session: Session = Depends(get_session)) -> list:
    """ returns all car data """
    query = select(Car)
    if size:
        query = query.where(Car.size == size)
    if doors:
        query = query.where(Car.doors >= doors)

    return session.exec(query).all()

@router.get("/api/cars/{id}")
def car_by_id(id: int, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        return car
    
    raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@router.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput, session: Session = Depends(get_session)) -> Car:
    new_car = Car.from_orm(car_input)
    session.add(new_car)
    session.commit()
    session.refresh(new_car)
    return new_car

@router.delete("api/cars/{id}", status_code=204)
def remove_car(id: int, session: Session = Depends(get_session)) -> None:
    car = session.get(Car, id)
    if car:
        session.delete(car)
        session.commit()
    
    raise HTTPException(status_code=404, detail=f"No car with id={id}.")
        
@router.put("/api/cars/{id}", response_model=CarOutput)
def change_car(id: int, new_data: CarInput, session: Session = Depends(get_session)) -> Car:
    car = session.get(Car, id)
    if car:
        car.fuel = new_data.fuel
        car.transmission = new_data.transmission
        car.size = new_data.size
        car.doors = new_data.doors
        session.commit()
        return car
    
    raise HTTPException(status_code=404, details=f"No car with id={id}.")

@router.post("/api/cars/{car_id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [ car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripInput(id=len(car.trips)+1,
                             start=trip.start, end=trip.end,
                             description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    
    raise HTTPException(status_code=404, detail=f"No car with id={id}.")
