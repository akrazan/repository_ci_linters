from typing import List

from fastapi import FastAPI, HTTPException
from sqlalchemy import select
from contextlib import asynccontextmanager

import models
import schemas
from database import engine, async_session_maker


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    yield  # приложение работает

    # SHUTDOWN
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/recipes/", response_model=schemas.RecipeOut)
async def create_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    """
    Ввод нового рецепта.
    in:
        {
        "name": название рецепта - строка в диапазоне 2-50 символов
        "description": описание рецепта - строка до 2000 символов
        "ingredients": список ингредиентов в виде строк, не допускается пустой список
        "preparation": время готовки в минутах
    }
    """
    new_recipe = models.Recipe(**recipe.model_dump())

    async with async_session_maker() as session:
        async with session.begin():
            session.add(new_recipe)
    return new_recipe


@app.get("/recipes/", response_model=List[schemas.RecipeOutList])
async def list_recipes() -> List[models.Recipe]:
    """
    Вывод списка рецептов.
    Рецепты отсортированы по популярности. В случае совпадения значений по времени готовки.
    """
    async with async_session_maker() as session:
        result = await session.execute(select(models.Recipe)
                                       .order_by(models.Recipe.views.desc(),
                                                 models.Recipe.preparation.asc()))
        recipes = result.scalars().all()
    return recipes


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int) -> models.Recipe:
    """
    Вывод рецепта с ID = recipe_id
    """
    async with async_session_maker() as session:
        result = await session.execute(select(models.Recipe).where(models.Recipe.id == recipe_id))
        recipe = result.scalar_one_or_none()
        recipe.views += 1
        await session.commit()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Рецепт не найден")
    return recipe
