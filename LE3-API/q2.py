"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 2: Get Full Sample Detail
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
from fastapi import FastAPI, HTTPException, Path
app = FastAPI(
    title="Metagenomics API",
    description="API for gene sequence of organisms found in the environments.",
    version="1.0.0"
)

#! path parameter
@app.get("/samples/{sample_id}")
async def full_sample_detail(
    sample_id: str = Path(
        description="e.g. SMP0001"
    )
):
    
    #! documentation
    """
        Get Full Sample Detail.
    """
    
    #! find sample
    formatted_sample_id = sample_id.upper()
    try:
        result = await collection.find_one(
            { "sample_id": formatted_sample_id }, 
            projection = {
                "_id": 0,
                "sample_id": 1,
                "location": 1,
                "collection_date": 1,
                "sequences": 1
            }
        )
    
    #! if sample not found
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=f"Sample '{sample_id}' does not exist."
        )
        
    #! arrange the output sequence
    ordered_result = {
        "sample_id": result.get("sample_id"),
        "location": result.get("location"),
        "collection_date": result.get("collection_date"),
        "sequences": result.get("sequences")
    }
    return ordered_result