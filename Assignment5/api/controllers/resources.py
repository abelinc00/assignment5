from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models import models, schemas


# Create Resource
def create(db: Session, resource: schemas.ResourceCreate):
    db_resource = models.Resource(item=resource.item, amount=resource.amount)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


# Read all Resources
def read_all(db: Session):
    return db.query(models.Resource).all()


# Read one Resource by ID
def read_one(db: Session, resource_id: int):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()


# Update Resource
def update(db: Session, resource: schemas.ResourceUpdate, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    if resource.item is not None:
        db_resource.item = resource.item
    if resource.amount is not None:
        db_resource.amount = resource.amount

    db.commit()
    db.refresh(db_resource)
    return db_resource


# Delete Resource
def delete(db: Session, resource_id: int):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    db.delete(db_resource)
    db.commit()
    return {"message": "Resource deleted successfully"}
