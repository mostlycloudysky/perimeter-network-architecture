import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


# Dependency
def get_db():
    db = models.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI in a DMZ-like setup!"}


@app.post("/items/", response_model=models.Item)
def create_item(item: models.Item, db: Session = Depends(get_db)):
    logger.info("Creating item: %s", item.name)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@app.get("/items/{item_id}", response_model=models.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    logger.info("Reading item with ID: %d", item_id)
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        logger.error("Item with ID %d not found", item_id)
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=models.Item)
def update_item(item_id: int, item: models.Item, db: Session = Depends(get_db)):
    logger.info("Updating item with ID: %d", item_id)
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        logger.error("Item with ID %d not found", item_id)
        raise HTTPException(status_code=404, detail="Item not found")
    db_item.name = item.name
    db_item.description = item.description
    db.commit()
    db.refresh(db_item)
    return db_item


@app.delete("/items/{item_id}", response_model=models.Item)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    logger.info("Deleting item with ID: %d", item_id)
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        logger.error("Item with ID %d not found", item_id)
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return item
