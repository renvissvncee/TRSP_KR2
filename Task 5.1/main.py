from fastapi import FastAPI, Response, Cookie, HTTPException

from pydantic import BaseModel, Field

import uuid 
from uuid import UUID

from itsdangerous import BadSignature, URLSafeSerializer

from datetime import datetime

SECRET_KEY = "super-secret-key"
serializer = URLSafeSerializer(SECRET_KEY)

app = FastAPI()

class User(BaseModel):
    id: UUID = Field(default_factory=uuid.uuid4)
    login: str
    password: str

user1 = User(login = "artem", password = "123")

users = [user1]

@app.post('/login')
def login(user: User, response: Response):
    for u in users:
        if u.login == user.login and u.password == user.password:
            user_id = str(u.id)
            issued_at = datetime.utcnow().timestamp()
            payload = { "user_id": user_id, "issued_at": issued_at }
            token = serializer.dumps(payload)
            response.set_cookie(key="session_token", value=token, max_age=300, httponly=True)
            return { "message": "Success" }
    raise HTTPException(status_code=401,detail="Invalid credentials")

@app.get('/profile')
def auth(response: Response, session_token: str | None = Cookie(default=None)):
    if not session_token:
        raise HTTPException(status_code=401,detail="Not authenticated")
    
    try:
        payload = serializer.loads(session_token)
    except BadSignature:
        raise HTTPException(status_code=401, detail="Invalid cookie")
    
    difference = (datetime.utcnow().timestamp() - payload["issued_at"])

    if difference > 300:
        raise HTTPException(status_code=401, detail="Invalid cookie")
    elif (difference > 180 and difference < 300):
        new_issued_at = datetime.utcnow().timestamp()
        new_payload = { "user_id": payload["user_id"], "issued_at": new_issued_at }
        new_token = serializer.dumps(new_payload)
        response.set_cookie(key="session_token", value=new_token, max_age=3600, httponly=True)
        return {
            "OLD:": session_token,
            "NEW:": new_token
        }
        

    for u in users:
        if str(u.id) == payload["user_id"]:
            return {"login": u.login}

    raise HTTPException(status_code=401, detail="User not found")


