"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 14: Sequence Length Statistics per Environment Type    
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
@app.get("/analytics/sequence-stats")
async def sequence_stats(
    environment_type: str | None = Query(
        default=None,
        description="Filter results by an environment type (e.g., Soil, Water)"
    )
):
    
    """
    Sequence Length Statistics per Environment Type
    """
    
    #! mongodb agregation pipeline
    pipeline = []
    
    if environment_type:
        environment_type = environment_type.capitalize()
        pipeline.append({
            "$match": { "environment_type": environment_type }
        })
        
    pipeline.extend([
        # Flatten sequence sub-document rows
        { "$unwind": "$sequences" },  
        { "$addFields": {
                "seq_length": { "$strLenCP": "$sequences.sequence" }
            }
        },        
        { "$group": {
                "_id": "$environment_type",
                "raw_avg": { "$avg": "$seq_length" },
                "min_length": { "$min": "$seq_length" },
                "max_length": { "$max": "$seq_length" },
                "total_sequences": { "$sum": 1 }
            }
        },        
        { "$project": {
                "_id": 0,
                "environment_type": "$_id",
                "avg_length": { "$round": ["$raw_avg", 1] },
                "min_length": 1,
                "max_length": 1,
                "total_sequences": 1
            }
        },        
        { "$sort": { "environment_type": 1 } }
    ])
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=10)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
        "data": [
            {
                "environment_type": result.get("environment_type"),
                "avg_length": result.get("avg_length"),
                "min_length": result.get("min_length"),
                "max_length": result.get("max_length"),
                "total_sequences": result.get("total_sequences")
            }
            for result in results
        ]
    }