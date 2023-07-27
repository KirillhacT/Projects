from fastapi import APIRouter, Request, Depends
from sqlalchemy import select

from .package import *
from app.database import async_session_maker
from app.bookings.schemas import SBooking
from app.bookings.dao import BookingDAO
from app.users.models import Users
from app.users.dependencies import get_current_user

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование"],
)

# @router.get("")
# async def get_bookings() -> list[SBooking]:
#     return await BookingDAO.find_all() 
#     # return await BookingDAO.find_by_id(2) 

@router.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all()

    