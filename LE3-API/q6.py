"""
    Name: NGU YU LING
    Matric No.: A23CS0149
    Question 6: List and Filter Taxonomy Records    
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
from fastapi import FastAPI, HTTPException, Query, Path
app = FastAPI(
    title="Metegenomics API",
    description="API for gene sequence of organisms found in the environments",
    version="1.0.0"
)

#! query parameters
@app.get("/taxonomy")
async def list_taxonomy(
    kingdom: str | None = Query(
        default = None,
        description="Filter by Bacteria or Archaea (query param on list endpoint)"
    )
):
    #! documentation
    """
        List Taxonomy Records
    """
        
    #! mongodb agregation pipeline
    pipeline = [
        { "$unwind": "$sequences" },
        { "$group": {
            "_id": "$sequences.taxonomy.taxonomy_id",
            "kingdom": { "$first": "$sequences.taxonomy.kingdom" },
            "phylum": { "$first": "$sequences.taxonomy.phylum" }
        }},
        { "$project": {
            "_id": 0,
            "taxonomy_id": "$_id",
            "kingdom": 1,
            "phylum": 1
        }}
    ]
    
    #! in case kingdom input available
    if kingdom:
        kingdom = kingdom.capitalize()
        pipeline.append(
            { "$match": { "kingdom": kingdom } }
        )
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return {
        "count": len(results),
        "data": [
            {
                "taxonomy_id": result.get("taxonomy_id"),
                "kingdom": result.get("kingdom"),
                "phylum": result.get("phylum")
            }
            for result in results
        ]  
    }


#! path parameters
@app.get("/taxonomy/{taxonomy_id}")
async def filter_taxonomy(
    taxonomy_id: str = Path(
        description="e.g. TAX005 (path param on detail endpoint)"
    )
):
    
    #! documentation
    """
        Filter Taxonomy Records 
    """
    
    #! filter
    taxonomy_id = taxonomy_id.upper()
    
    #! mongodb aggregation pipeline
    pipeline = [
        { "$unwind": "$sequences" },
        { "$match":
            { "sequences.taxonomy.taxonomy_id": taxonomy_id }
        },
        { "$group": {
            "_id": "$sequences.taxonomy.taxonomy_id",
            "kingdom": { "$first": "$sequences.taxonomy.kingdom" },
            "phylum": { "$first": "$sequences.taxonomy.phylum" },
            "class": { "$first": "$sequences.taxonomy.class" },
            "order": { "$first": "$sequences.taxonomy.order" },
            "family": { "$first": "$sequences.taxonomy.family" },
            "genus": { "$first": "$sequences.taxonomy.genus" },
            "species": { "$first": "$sequences.taxonomy.species" }
            }
        },
        { "$project": {
            "_id": 0,
            "taxonomy_id": "$_id",
            "kingdom": 1,
            "phylum": 1,
            "class": 1,
            "order": 1,
            "family": 1,
            "genus": 1,
            "species": 1,
            }
        }
    ]
    
    #! execute pipeline
    try:
        cursor = collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #! if taxonomy id is not found
    if not result:
        raise HTTPException(status_code=404, detail=f"Taxonomy ID {taxonomy_id} not found.")
    
    return {
        "Detail": {
            "taxonomy_id": result[0].get("taxonomy_id"),
            "kingdom": result[0].get("kingdom"),
            "phylum": result[0].get("phylum"),
            "class": result[0].get("class"),
            "order": result[0].get("order"),
            "family": result[0].get("family"),
            "genus": result[0].get("genus"),
            "species": result[0].get("species")
        }
    }