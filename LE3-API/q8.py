"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 8: Sample Collection Trend Over Time    
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
from datetime import datetime
app = FastAPI(
    title="Metegenomics API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! query parameters
@app.get("/analytics/trend")
async def sample_trend(
    start_date: str = Query(
        description="Range start date inclusive (YYYY-MM-DD)"
    ),
    end_date: str = Query(
        description="Range end date inclusive (YYYY-MM-DD)"
    )
):
    """
    Sample Collection Trend Over Time
    """
    
    #! check if start_date > end_date
    if start_date > end_date:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid date range: start_date '{start_date}' cannot be chronologically after end_date '{end_date}'."
        )
        
    #! mongodb aggregation pipeline
    pipeline = [
        { "$addFields": {
                "parsed_collection_date": {
                    "$dateFromString": { "dateString": "$collection_date" }
                }
            }
        },
        { "$match": {
                "parsed_collection_date": {
                    "$gte": datetime.strptime(start_date, "%Y-%m-%d"),
                    "$lte": datetime.strptime(end_date, "%Y-%m-%d")
                }
            }
        },
        { "$group": {
                "_id": {
                    "year": { "$year": "$parsed_collection_date" },
                    "month": { "$month": "$parsed_collection_date" }
                },
                "count": { "$sum": 1 }
            }
        },
        { "$project": {
                "_id": 0,
                "year": "$_id.year",
                "month": "$_id.month",
                "count": 1
            }
        },
        { "$sort": { "year": 1, "month": 1 } }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
    #! return response matching the target model structure requirements
    return {
        "start_date": start_date,
        "end_date": end_date,
        "data": [
            {
                "year": trend.get("year"),
                "month": trend.get("month"),
                "count": trend.get("count")
            }
            for trend in results
        ]
    }