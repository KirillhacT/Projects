from sqlalchemy import Column, Text, Integer, ForeignKey, String, Date
from sqlalchemy.orm import relationship
from app.database import Base

class Genres(Base):
    __tablename__ = "genres"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(20), nullable=False)  

    post = relationship("Posts", back_populates="genre")

    def __str__(self) -> str:
        return str(self.title)


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(40), nullable=False)
    release_date = Column(Date, nullable=False)
    description = Column(Text, nullable=False)
    series_count = Column(Integer, nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id"))
    image_id = Column(Integer)

    genre = relationship("Genres", back_populates="post")

    def __str__(self) -> str:
        return str(self.title)

    
    
    