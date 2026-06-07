from fastapi import FastAPI

app = FastAPI()

# route for default url
@app.get("/")
async def root():
    return {"message": "Hello World"}

# path parameter
@app.get("/itmes/{item_id}") #value in {} will be passed into the function
async def read_item(item_id):
    return {"item_id": item_id}

# path parameter with type
@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# query parameter
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
@app.get("/items/")
async def read_item(skip: int=0, limit: int=10):
    return fake_items_db[skip: skip+limit]

# enhance documentation
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(openai_tags=tags_metadata)
@app.get("/users/", tags=["users"]) # use the tag specified in tags_metadata
async def get_users():
    return [{"name": "Harry"}, {"Name": "Ron"}]

@app.get("/items/", tags=["items"]) # use the tag specified in tags_metadata
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]