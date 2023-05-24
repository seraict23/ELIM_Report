from fastapi import FastAPI, Query, Path, HTTPException, status
from typing import Optional
from pydantic import BaseModel

app=FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None

inventory={}

@app.get("/get_item/{item_id}")
def get_item(item_id: int):
    # Give a detailed information to user about path parameters (None=Default value(required))
    return inventory[item_id]

@app.get("/get_by_name/{item_id}")
def get_by_name(item_id: int, test: int, name: Optional[str]=None):
# def get_by_name(*, name: Optional[str]=None, test: int)
    for item_id in inventory:    
        if inventory[item_id].name==name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item ID not found.")

@app.post("/create_item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED, detail="Item ID alreday exists.")
    inventory[item_id]=item
    return inventory[item_id]

@app.put("/update_item/{item_id}")
def update_item(item_id: int, item: UpdateItem):
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    if item.name != None:
        inventory[item_id].name=item.name
    if item.price != None:
        inventory[item_id].price=item.price
    if item.brand != None:
        inventory[item_id].brand=item.brand
    return inventory[item_id]

@app.delete("/delete_item")
def delete_item(item_id: int = Query(..., description="The ID of the item to delete, ge=0")):
    # ...(ellipsis): in here, item_id is required query parameters
    if item_id not in inventory:
        raise HTTPException(status_code=404, detail="Item ID does not exist.")
    
    del inventory [item_id]
    return {"Success": "Item deleted."}