"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 15: Multi-filter Analytical Summary per Sample    
"""

#! connect to mongodb
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query

load_dotenv()
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client["metagenomics"]
collection = db["genomes"]

#! create fastapi app instance
app = FastAPI(
    title="Metegenomics API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! query parameters
@app.get("/samples/summary")
async def samples_summary(
    country: str | None = Query(default=None, description="Filter by country"),
    environment_type: str | None = Query(default=None, description="Filter by environment type"),
    start_date: str | None = Query(default=None, description="Collection date range start (YYYY-MM-DD)"),
    end_date: str | None = Query(default=None, description="Collection date range end (YYYY-MM-DD)"),
    min_sequences: int = Query(default=1, ge=1, description="Only return samples with at least this many sequences")
):
    
    """
    Multi-filter Analytical Summary per Sample
    """
    
    #! if start_date > end_date
    if start_date and end_date and start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid Range: start_date '{start_date}' cannot be after end_date '{end_date}'."
        )

    #! filter
    match_filter = {}
    if country:
        match_filter["location.country"] = {"$regex": country, "$options": "i"}
    if environment_type:
        match_filter["environment_type"] = environment_type.capitalize()        
    if start_date or end_date:
        date_cond = {}
        if start_date:
            date_cond["$gte"] = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            date_cond["$lte"] = datetime.strptime(end_date, "%Y-%m-%d")
            
    
    #! mongodb aggregation pipeline
    pipeline = []

    pipeline.append({
        "$addFields": {
            "parsed_collection_date": { "$dateFromString": { "dateString": "$collection_date" } }
        }
    })
    
    if start_date or end_date:
        match_filter["parsed_collection_date"] = date_cond
        
    pipeline.append({ "$match": match_filter })
    
    pipeline.extend([
        { "$unwind": "$sequences" },        
        { "$group": {
                "_id": {
                    "sample_id": "$sample_id",
                    "species": "$sequences.taxonomy.species"
                },
                "species_occurrence_count": { "$sum": 1 },
                "location": { "$first": "$location" },
                "collection_date": { "$first": "$collection_date" },
                "environment_type": { "$first": "$environment_type" }
            }
        },        
        { "$sort": { "_id.sample_id": 1, "species_occurrence_count": -1 } },        
        { "$group": {
                "_id": "$_id.sample_id",
                "location": { "$first": "$location" },
                "collection_date": { "$first": "$collection_date" },
                "environment_type": { "$first": "$environment_type" },                
                "sequence_count": { "$sum": "$species_occurrence_count" },                
                "distinct_species_count": { "$sum": 1 },                
                "dominant_species": { "$first": "$_id.species" }
            }
        },        
        { "$match": {
                "sequence_count": { "$gte": min_sequences }
            }
        },        
        { "$project": {
                "_id": 0,
                "sample_id": "$_id",
                "location": 1,
                "collection_date": 1,
                "environment_type": 1,
                "sequence_count": 1,
                "distinct_species_count": 1,
                "dominant_species": 1
            }
        },        
        { "$sort": { "sample_id": 1 } }
    ])
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    return {
        "filters_applied": {
            "country": country,
            "environment_type": environment_type,
            "start_date": start_date,
            "end_date": end_date,
            "min_sequences": min_sequences
        },
        "count": len(results),
        "data": [
            {
                "sample_id": result.get("sample_id"),
                "location": result.get("location"),
                "collection_date": result.get("collection_date"),
                "environment_type": result.get("environment_type"),
                "sequence_count": result.get("sequence_count"),
                "distinct_species_count": result.get("distinct_species_count"),
                "dominant_species": result.get("dominant_species")
            }
            for result in results
        ]
    }