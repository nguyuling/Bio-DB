"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 9: Top N Most Frequently Occurring Species    
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
@app.get("/analytics/top-species")
async def top_species(
    n: int = Query(
        default=10,
        ge=1,
        description="Number of top species to return (default 10, max 20)"
    )
):
    """
    Top N Most Frequently Occurring Species
    """
    
    #! mongodb aggregation pipeline
    pipeline = [
        { "$unwind": "$sequences" },
        { "$group": {
                "_id": "$sequences.taxonomy.species",
                "count": { "$sum": 1 },
                "genus": { "$first": "$sequences.taxonomy.genus" },
                "phylum": { "$first": "$sequences.taxonomy.phylum" },
                "kingdom": { "$first": "$sequences.taxonomy.kingdom" }
            }
        },
        { "$sort": { "count": -1 } },
        { "$limit": min(n, 20) },        
        { "$project": {
                "_id": 0,
                "species": "$_id",
                "genus": 1,
                "phylum": 1,
                "kingdom": 1,
                "count": 1
            }
        }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=min(n, 20))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! arrange result
    ordered_results = [
        {
            "rank": index,
            "species": result.get("species"),
            "genus": result.get("genus"),
            "phylum": result.get("phylum"),
            "kingdom": result.get("kingdom"),
            "count": result.get("count")
        }
        for index, result in enumerate(results, start=1)
    ]
    
    return {
        "n": min(n, 20),
        "data": ordered_results
    }