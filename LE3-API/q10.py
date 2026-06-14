"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 10: Find Samples Containing a Specific Species    
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
    title="Metegenomics API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! query parameters
@app.get("/analytics/species-search")
async def species_search(
    species: str = Query(
        description="Exact or partial species name (case-insensitive)"
    )
):
    
    """
    Find Samples Containing a Specific Species
    """
    
    #! mongodb aggregation pipeline
    pipeline = [
        # Step 1: Flatten sequences array to evaluate each individual entry
        { "$unwind": "$sequences" },        
        { "$match": { 
                "sequences.taxonomy.species": { "$regex": species, "$options": "i" } 
            } 
        },
        { "$group": {
                "_id": "$sample_id",
                "location": { "$first": "$location" },
                "environment_type": { "$first": "$environment_type" },
                "matching_sequence_ids": { "$addToSet": "$sequences.sequence_id" }
            }
        },        
        {
            "$project": {
                "_id": 0,
                "sample_id": "$_id",
                "location": 1,
                "environment_type": 1,
                "matching_sequence_ids": 1
            }
        }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! arrange result
    ordered_results = [
        {
            "sample_id": result.get("sample_id"),
            "location": result.get("location"),
            "environment_type": result.get("environment_type"),
            "matching_sequence_ids": result.get("matching_sequence_ids")
        }
        for result in results
    ]
    
    return {
        "species": species,
        "sample_count": len(ordered_results),
        "data": ordered_results
    }