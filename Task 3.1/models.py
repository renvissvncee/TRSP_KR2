from pydantic import BaseModel, Field, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    age: int 
    is_subscribed: bool