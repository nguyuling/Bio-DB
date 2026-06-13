"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 4: Search Samples by Location
"""

#! connect to mongodb
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["metagenomics"]
collection = db["genomes"]

#! create fastapi app insatnce
from fastapi import FastAPI, HTTPException, Query
app = FastAPI(
    title="Metagenomcs API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! query parameters
@app.get("/samples/search")
async def samples_by_location(
    country: str | None = Query(
        default=None,
        description="e.g. Malaysia, sweden (case-insensitive"
    ),
    city: str | None = Query(
        default=None,
        description="e.g. Manaus (case-insensitive)"
    )
):
    
    #! documentation
    """
        Search Samples by Location
    """
    
    #! if no input is provided
    if not country and not city:
        raise HTTPException(status_code=400, detail="Neither country nor city is supplied.")
    
    #! filter
    match_filter = {}
    if country:
        match_filter["location.country"] = { "$regex": country, "$options": "i" }
    if city:
        match_filter["location.city"] = { "$regex": city, "$options": "i" }
    
    #! find sample
    try:
        cursor = collection.find(
            match_filter,
            projection={
                "_id": 0,
                "sample_id": 1,
                "location": 1,
                "environment_type": 1,
                "collection_date": 1,
                "sequences": 1
            }
        )    
        result = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #! arrange the output
    ordered_result = [
        {
            "sample_id": sample.get("sample_id"),
            "location": sample.get("location"),
            "environment_type": sample.get("environment_type"),
            "collection_date": sample.get("collection_date"),
            "sequences": sample.get("sequences")
        }
        for sample in result
    ]
    return {
        "count": len(result),
        "data": ordered_result
    }