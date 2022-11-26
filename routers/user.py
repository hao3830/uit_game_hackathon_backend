from fastapi import APIRouter, Form

from src.models.user.user import User
from src.rcode import rcode

router = APIRouter()


@router.get("/")
def get_user_info(
    user_name: str,
    password: str,
):
    err, user = User.get(user_name=user_name,password=password)

    if err:
        return rcode(err)
    
    return {
        **rcode(1000),
        'user': user
    }

@router.post("/register")
def register(
    user_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):  
    user = User(name=user_name,email=email,password=password)
    err, user = User.insert(user)
    
    if err:
        return rcode(err)
    
    return {
        **rcode(1000),
        'user': user
        }

@router.get("/list_user")
def get_list_user(
    top: int = 20
):
    err, users = User.get_all(top)

    if err:
        return rcode(err)
    
    return {
        **rcode(1000),
        'users':users
    }

