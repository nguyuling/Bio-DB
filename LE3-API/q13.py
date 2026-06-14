"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 13: Phylum Distribution for a Specific Location    
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
@app.get("/analytics/phylum-by-location")
async def phylum_by_location(
    city: str = Query(
        description="e.g. Manaus (case-insensitive)"
    ),
    country: str = Query(
        description="e.g. Brazil (case-insensitive)"
    )
):
   
    """
    Phylum Distribution for a Specific Location
    """
    
    #! mongodb aggregation pipeline
    pipeline = [
        { "$match": {
                "location.city": { "$regex": city, "$options": "i" },
                "location.country": { "$regex": country, "$options": "i" }
            }
        },
        { "$unwind": "$sequences" },
        { "$group": {
                "_id": "$sequences.taxonomy.phylum",
                "count": { "$sum": 1 }
            }
        },
        { "$sort": { "count": -1 } },        
        { "$project": {
                "_id": 0,
                "phylum": "$_id",
                "count": 1
            }
        }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! is no result found
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No microbiome samples found for location: {city.title()}, {country.title()}."
        )
            
    return {
        "location": {
            "city": city.title(),
            "country": country.title()
        },
        "total_sequences": sum(item.get("count", 0) for item in results),
        "phylum_breakdown": [
            {
                "phylum": result.get("phylum"),
                "count": result.get("count")
            }
            for result in results
        ]
    }