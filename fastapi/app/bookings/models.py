from sqlalchemy import JSON, Column, Integer, String, ForeignKey, Date, Computed
from app.database import Base

class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_from - date_to) * price"))
    total_days = Column(Integer, Computed("date_from - date_to"))