"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 12: Samples Exceeding Species Diversity Threshold    
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
@app.get("/analytics/diverse-samples")
async def diverse_samples(
    min_species: int = Query(
        description="Minimum number of distinct species in a sample"
    )
):
    
    """
    Samples Exceeding Species Diversity Threshold
    """
    
    #! if min_species < 1 
    if min_species < 1:
        raise HTTPException(
            status_code=422,
            detail=f"Validation Error: The requested threshold min_species ({min_species}) cannot be less than 1."
        )
        
    #! mongodb aggregation pipeline
    pipeline = [
        { "$unwind": "$sequences" },        
        { "$group": {
                "_id": "$sample_id",
                "location": { "$first": "$location" },
                "environment_type": { "$first": "$environment_type" },
                "unique_species_set": { "$addToSet": "$sequences.taxonomy.species" }
            }
        },        
        { "$project": {
                "_id": 0,
                "sample_id": "$_id",
                "location": 1,
                "environment_type": 1,
                "distinct_species_count": { "$size": "$unique_species_set" }
            }
        },        
        { "$match": {
                "distinct_species_count": { "$gte": min_species }
            }
        }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! Transform results to follow strict dictionary structural output expectations
    ordered_results = [
        {
            "sample_id": result.get("sample_id"),
            "location": result.get("location"),
            "environment_type": result.get("environment_type"),
            "distinct_species_count": result.get("distinct_species_count")
        }
        for result in results
    ]
    
    return {
        "min_species": min_species,
        "count": len(ordered_results),
        "data": ordered_results
    }