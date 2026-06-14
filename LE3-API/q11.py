"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 11: Microbial Kingdom Breakdown by Country    
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
@app.get("/analytics/kingdom-by-country")
async def kingdom_by_country(
    country: str | None = Query(
        default=None,
        description="Filter results for a specific country (e.g., Brazil, Sweden)"
    )
):
    
    """
    Microbial Kingdom Breakdown by Country
    """
    
    #! mongodb aggregation pipeline
    pipeline = []

    if country:
        formatted_country = country.title()
        pipeline.append({
            "$match": { "location.country": formatted_country }
        })
        
    pipeline.extend([
        { "$unwind": "$sequences" },
        { "$group": {
                "_id": "$location.country",                
                "Bacteria": {
                    "$sum": {
                        "$cond": [
                            { "$eq": ["$sequences.taxonomy.kingdom", "Bacteria"] }, 1, 0
                        ]
                    }
                },                
                "Archaea": {
                    "$sum": {
                        "$cond": [
                            { "$eq": ["$sequences.taxonomy.kingdom", "Archaea"] }, 1, 0
                        ]
                    }
                }
            }
        },
        { "$project": {
                "_id": 0,
                "country": "$_id",
                "Bacteria": 1,
                "Archaea": 1
            }
        },
        { "$sort": { "country": 1 } }
    ])
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! Map outputs to match the strict schema key ordering
    return {
        "data": [
            {
                "country": result.get("country"),
                "Bacteria": result.get("Bacteria"),
                "Archaea": result.get("Archaea")
            }
            for result in results
        ]
    }