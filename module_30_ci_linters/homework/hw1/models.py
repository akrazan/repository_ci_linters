from sqlalchemy import Column, String, Integer, JSON
from database import Base

class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), index=True, nullable=False)
    description = Column(String(2000))

    # Храним список ингредиентов как JSON — сразу совместим с Pydantic list[str]
    ingredients = Column(JSON, nullable=False, default=list)

    preparation = Column(Integer, default=0)
    views = Column(Integer, default=0)
