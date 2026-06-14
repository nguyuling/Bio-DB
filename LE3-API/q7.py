"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 7: Species Diversity per Environment Type    
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
@app.get("/analytics/diversity")
async def species_diversity(
    environment_type: str | None = Query(
        default=None,
        description="Filter results by an environment type (e.g., Soil, Water)"
    )
):
    """
    Species Diversity per Environment Type
    """
    
    #! mongodb aggregation pipeline
    pipeline = []
    
    if environment_type:
        environment_type = environment_type.capitalize()
        pipeline.append({
            "$match": { "environment_type": environment_type }
        })
        
    pipeline.extend([
        { "$unwind": "$sequences" },
        { "$group": {
                "_id": "$environment_type",
                "distinct_species": { "$addToSet": "$sequences.taxonomy.species" }
            }
        },
        { "$project": {
                "_id": 0,
                "environment_type": "$_id",
                "unique_species_count": { "$size": "$distinct_species" }
            }
        }
    ])
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! return block with ordered field output format
    return {
        "data": [{
                "environment_type": result.get("environment_type"),
                "unique_species_count": result.get("unique_species_count")
            }
            for result in results
        ]
    }