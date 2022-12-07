import json
from sqlmodel import SQLModel, Field, Relationship
from passlib.context import CryptContext


class TripInput(SQLModel):
    start: int
    end: int
    description: str
    
class TripOutput(TripInput):
    id: int

class CarInput(SQLModel):
    size: str
    fuel: str | None = "electric"
    doors: int
    transmission: str | None = "auto"
    
    class Config:
        schema_extra = {
            "example": {
                "size": "m",
                "doors": 5,
                "transmission": "manual",
                "fuel": "hybrid"
            }
        }
    
class Car(CarInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    

pwd_context = CryptContext(schemes=["bcrypt"])
    
class CarOutput(CarInput):
    id: int
    trips: list[TripOutput] = []
    
class UserOutput(SQLModel):
    id: int
    username: str

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str
    password_hash: str = ""
    
    def set_password(self, password):
        """Setting the passwords actually sets password_hash."""
        self.password_hash = pwd_context.hash(password)
        
    def verify_password(self, password):
        """Verify given password by hashing and comparing to password_hash"""
        return pwd_context.verify(password, self.password_hash)
    
def load_db() -> list[CarOutput]:
    """Load a list of Car objects from a JSON file"""
    with open("cars.json") as f:
        return [CarOutput.parse_obj(obj) for obj in json.load(f)]

def save_db(cars: list[CarOutput]):
    """save a list of Car objects from a JSON file"""
    with open("cars.json", "w") as f:
        json.dump([car.dict() for car in cars], f, indent=4)