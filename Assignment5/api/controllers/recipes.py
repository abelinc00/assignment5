from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import models, schemas


# Create Recipe
def create(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(
        sandwich_id=recipe.sandwich_id,
        resource_id=recipe.resource_id,
        amount=recipe.amount
    )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


# Read all Recipes
def read_all(db: Session):
    return db.query(models.Recipe).all()


# Read one Recipe by ID
def read_one(db: Session, recipe_id: int):
    return db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()


# Update Recipe
def update(db: Session, recipe: schemas.RecipeUpdate, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if recipe.sandwich_id is not None:
        db_recipe.sandwich_id = recipe.sandwich_id
    if recipe.resource_id is not None:
        db_recipe.resource_id = recipe.resource_id
    if recipe.amount is not None:
        db_recipe.amount = recipe.amount

    db.commit()
    db.refresh(db_recipe)
    return db_recipe


# Delete Recipe
def delete(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(db_recipe)
    db.commit()
    return {"message": "Recipe deleted successfully"}
