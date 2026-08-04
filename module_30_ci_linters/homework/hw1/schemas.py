from typing import List

from pydantic import BaseModel, Field, field_validator


class BaseRecipe(BaseModel):
    name: str = Field(..., description="Название рецепта", min_length=2, max_length=50)


class RecipeIn(BaseRecipe):
    """
    Ввод нового рецепта.
    """
    description: str = Field("", description="Описание приготовления рецепта", max_length=2000)
    ingredients: list[str] = Field(default_factory=list, description="Список ингредиентов")
    preparation: int = Field(default=0, ge=0, description="Время приготовления в минутах")
    views: int = Field(default=0, ge=0, description="Количество просмотров")

    @field_validator("ingredients")
    @classmethod
    def ensure_non_empty(cls, v: List[str]) -> List[str]:
        # валидация списка ингредиентов, который не должен быть пустым
        if not v:
            raise ValueError("Список ингредиентов не может быть пустым")
        return v


class RecipeOutList(BaseRecipe):
    """
    Таблица со списком всех рецептов в базе.
    Поля:
        название
        количество просмотров
        время готовки (в минутах)
    """
    preparation: int
    views: int

    class Config:
        from_attributes = True


class RecipeOut(BaseRecipe):
    """
    Детальная информация по каждому рецепту:
    Поля:
        название
        время готовки
        список ингредиентов
        текстовое описание
    """
    preparation: int
    ingredients: list[str]
    description: str

    class Config:
        from_attributes = True
