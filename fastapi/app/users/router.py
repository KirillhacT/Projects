from fastapi import APIRouter, Response, Depends
from app.users.schemas import SUserAuth
from app.users.auth import authenticate_user, get_password_hash, create_acces_token
from app.users.models import Users
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user, get_admin_user
from app.exceptions import UserAlreadyExistException, IncorrectEmailOrPasswordException
from pydantic import EmailStr

router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)

@router.post("/register")
async def register_user(user_data: SUserAuth) -> None:
    exsting_user = await UserDAO.find_one_ore_none(email=user_data.email)
    if exsting_user:
        raise UserAlreadyExistException
    hashed_password = get_password_hash(user_data.password)
    await UserDAO.add(email=user_data.email, hashed_password=hashed_password, role="User")
    
@router.post("/login")
async def login_user(responce: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_acces_token({"sub": str(user.id)})
    responce.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token

@router.post("/logout")
async def logout_user(responce: Response):
    responce.delete_cookie("booking_access_token")

@router.get("/me")
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.post("/set-admin")
async def set_admin(
    email: EmailStr,
    user = Depends(get_admin_user)
) -> None:
    await UserDAO.update_role(email, "Admin")
    

    
    
            



