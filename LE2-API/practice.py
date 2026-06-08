import os
from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title="Airbnb Price Analysis API",
    description="API to calculate average Airbnb listing prices from MongoDB Atlas.",
    version="1.0.0"
)

# MongoDB connection setup
MONGO_URI = "mongodb+srv://dbAdmin:123abc@cluster0.dklylwy.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client["sample_airbnb"]
collection = db["listingsAndReview"]


# Endpoint: average price by city / market
@app.get("/prices/by-city")
async def get_average_price_by_city():
    """
    Calculate the average listing price grouped by city (market).
    """
    pipeline = [
        {
            "$group": {
                "_id": "$address.market",
                "average_price": { "$avg": "$price" }
            }
        },
        {
            "$sort": { "_id": 1 }
        }
    ]
    
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100) # limits to top 100 cities
        formatted_results = []
        for doc in results:
            # skip records where the city name might be blank or null
            if doc["_id"]: 
                formatted_results.append({
                    "city": doc["_id"],
                    # Convert MongoDB Decimal128 into a clean Python float rounded to 2 decimals
                    "avg_price": round(float(str(doc["average_price"])), 2)
                })
        return {"count": len(formatted_results), "data": formatted_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint: average price by country
@app.get("/prices/by-country")
async def get_average_price_by_country():
    """
    Calculate the average listing price grouped by country.
    """
    pipeline = [
        {
            "$group": {
                "_id": "$address.country",
                "average_price": { "$avg": "$price" }
            }
        },
        {
            "$sort": { "average_price": -1 }
        }
    ]
    
    try:
        cursor = collection.aggregate(pipeline)
        results = await cursor.to_list(length=100)
        formatted_results = []
        for doc in results:
            if doc["_id"]:
                formatted_results.append({
                    "country": doc["_id"],
                    "avg_price": round(float(str(doc["average_price"])), 2)
                })
        return {"count": len(formatted_results), "data": formatted_results}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))