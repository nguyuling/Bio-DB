"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 5: Get a Single Sequence by ID    
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
    title="Metegenomics API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! path parameters
@app.get("/sequences/{sequence_id}")
async def sequence(
    sequence_id: str = Path(
        description="e.g. SEQ000042"
    )
):
    
    #! documentation
    """
        Get a Single Sequence by ID
    """
    
    #! find sequence
    seq_id = sequence_id.upper()
        
    #! mongodb aggregation pipeline
    pipeline = [
        { "$unwind": "$sequences" },
        { "$match": { "sequences.sequence_id": seq_id } },
        { "$project": {
            "_id": 0,
            "sequence_id": "$sequences.sequence_id",
            "sample_id": 1,
            "sequence": "$sequences.sequence",
            "taxonomy": "$sequences.taxonomy"
        }}
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #! if sequence is not found
    if not result:
        raise HTTPException(status_code=404, detail=f"Sequence {sequence_id} not found.")
    
    return {
        "sequence_id": result[0].get("sequence_id"),
        "sample_id": result[0].get("sample_id"),
        "sequence": result[0].get("sequence"),
        "taxonomy": result[0].get("taxonomy")
    }