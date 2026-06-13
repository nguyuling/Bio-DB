"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 1: List Samples with Filtering and Pagination  
"""

#! connect to mongodb
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["metagenomics"]
collection = db["genomes"]

#! create fastapi app instance
from fastapi import FastAPI, HTTPException, Query
app = FastAPI(
    title="Metagenomics API",
    description="API for gene sequence of organisms found in the environments.",
    version="1.0.0"
)

#! query parameters
@app.get("/samples")
async def list_samples(
    page: int | None = Query(
        default = 1,
        description = "Page number (1-indexed)"
    ),
    limit: int | None = Query(
        default = 20,
        description = "Number of results per page (max 100)"
    ),
    environment_type: str | None = Query (
        default = None,
        description = "Filter by Soil, Water, Air, or Sediment"
    )
):
    
    # documentation
    """
    List Samples with Filtering and Pagination.
    """
    
    #! filter
    match_filter = {}
    if environment_type:
        match_filter["environment_type"] = environment_type.capitalize()
        
    #! mongodb aggregation pipeline
    pipeline = [
        { "$match": match_filter },
        { "$skip": (page-1) * limit },
        { "$limit": limit },
        { "$project": {
                "_id": 0,
                "sample_id": 1,
                "location": 1,
                "collection_date": 1,
                "environment_type": 1,
                "sequence_count": { "$size": "$sequences" }
            }
        }
    ]
    
    #! read user input
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=limit)        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    #! return output
    return {
        "total": await collection.count_documents({}),
        "page": page,
        "limit": limit,
        "data": results
    }