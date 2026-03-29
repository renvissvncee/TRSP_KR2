from fastapi import FastAPI
from models import User

app = FastAPI()

@app.post('/create_user')
def create_user(user: User):
    if (not user.name):
        return {"error": "Введите имя"}
    
    if (not user.email):
        return {"error": "Введите почту"}
    
    if (user.age <= 0):
       return {"error": "Возраст должен быть положительным"} 
    
    return {
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "is_subscribed": user.is_subscribed
    }
    
