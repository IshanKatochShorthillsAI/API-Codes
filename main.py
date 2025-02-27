from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List

app = FastAPI()


# Define the Item model with an extra field for demonstration
class Item(BaseModel):
    name: str = Field(..., example="Sample Item")
    description: str = Field(..., example="A detailed description of the sample item.")
    price: float = Field(..., gt=0, example=9.99)


# In-memory storage for items
items: Dict[int, Item] = {}


# Endpoint to create a new item
@app.post("/items/", response_model=dict)
def create_item(item: Item):
    item_id = len(items) + 1
    items[item_id] = item
    return {"id": item_id, **item.dict()}


# Endpoint to retrieve a list of all items
@app.get("/items/", response_model=List[dict])
def get_all_items():
    result = []
    for item_id, item in items.items():
        result.append({"id": item_id, **item.dict()})
    return result


# Endpoint to retrieve a specific item by ID
@app.get("/items/{item_id}", response_model=dict)
def get_item(item_id: int):
    if item_id in items:
        return {"id": item_id, **items[item_id].dict()}
    raise HTTPException(status_code=404, detail="Item not found")


# Endpoint to update an existing item by ID
@app.put("/items/{item_id}", response_model=dict)
def update_item(item_id: int, updated_item: Item):
    if item_id in items:
        items[item_id] = updated_item
        return {"id": item_id, **updated_item.dict()}
    raise HTTPException(status_code=404, detail="Item not found")


# Endpoint to delete an item by ID
@app.delete("/items/{item_id}", response_model=dict)
def delete_item(item_id: int):
    if item_id in items:
        del items[item_id]
        return {"detail": "Item deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
