"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 3: Get Sequences for a Sample
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
    title="Metagenomic API",
    description="API for gene sequence of organisms found in the environments.",
    version="1.0.0"
)

#! path parameter
@app.get("/samples/{sample_id}/sequences")
async def sample_sequences(
    sample_id: str = Path(
        description="e.g. SMP0042"
    )
):
    
    #! documentation
    """
        Get Sequences for a Sample
    """
    
    #! find sample
    formatted_sample_id = sample_id.upper()
    try:
        result = await collection.find_one(
            { "sample_id": formatted_sample_id },
            projection = {
                "_id": 0,
                "sample_id": 1,
                "sequences": 1
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, details=str(e))
    
    #! if sample not found
    if result is None:
        raise HTTPException(
            status_code=404,
            detail=f"Sample {"sample_id"} does not exist"
        )
    
    #! arrange the output
    return {
        "sample_id": result.get("sample_id"),
        "sequence_count": len(result.get("sequences", [])), # Done directly in Python!
        "sequences": result.get("sequences")
    }