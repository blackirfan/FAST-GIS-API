from fastapi import FastAPI, HTTPException
from models import PersonalInfo, LocationFeatureCollection
from models import PersonalInfo, LocationFeatureCollection, LocationFeature, GeoJSONPoint, GeoJSONPolygon, GeoJSONMultiPolygon, LocationProperties, MonglaFeatureCollection, ObservationFeatureCollection, ObservationFeature, ObservationProperties
from data import personal_info, location_collection, zone_collection
from db import database
import json
import httpx

tags_metadata = [
    {
        "name": "Personal Info",
        "description": "Operations related to retrieving **personal information**.",
    },
    {
        "name": "GIS Data",
        "description": "Operations strictly related to **geospatial data** in standard GeoJSON format.",
    },
]

app = FastAPI(
    title="Personal GIS Portfolio API",
    description="""
    API serving personal information and geospatial data. 
    
    ## Features
    * Retrieve Developer Profile
    * Get Key Locations in GeoJSON
    """,
    version="1.0.0",
    openapi_tags=tags_metadata
)

@app.on_event("startup")
async def startup():
    try:
        await database.connect()
    except Exception as e:
        print(f"Failed to connect to database: {e}")

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/", tags=["General"])
async def root():
    return {"message": "Welcome to my Personal GIS Portfolio API. Visit /docs for more info."}

@app.get("/me", response_model=PersonalInfo, tags=["Personal Info"], summary="Get Profile")
async def get_personal_info():
    """
    Get personal information about the developer.
    
    - **name**: Full Name
    - **role**: Current Title
    - **bio**: Professional Biography
    - **contact_email**: Email address
    """
    return personal_info

@app.get("/locations", response_model=LocationFeatureCollection, tags=["GIS Data"], summary="Get GeoJSON Locations")
async def get_locations():
    """
    Get a GeoJSON FeatureCollection of interesting locations.
    
    Returns a standard **FeatureCollection** compatible with Mapbox, Leaflet, or OpenLayers.
    """
    return location_collection

@app.get("/zones", response_model=LocationFeatureCollection, tags=["GIS Data"], summary="Get GeoJSON Zones")
async def get_zones():
    """
    Get a GeoJSON FeatureCollection of interesting zones (Polygons).
    """
    return zone_collection

@app.get("/mongla-upzila", response_model=MonglaFeatureCollection, tags=["GIS Data"], summary="Get Mongla Upzila Data")
async def get_mongla_upzila():
    """
    Get GIS data from the **mongla_upazila** table.
    
    This endpoint directly queries the PostgreSQL database using PostGIS `ST_AsGeoJSON`.
    """
    # Query to fetch all rows and convert the 'geom' column to GeoJSON
    # Using 'geom' as the standard PostGIS geometry column name.
    # We construct the FeatureCollection manually or return a list of features.
    # Ideally, we should construct a valid GeoJSON FeatureCollection.
    
    query = """
        SELECT 
            id, 
            ST_AsGeoJSON(geom) as geometry, 
            adm3_en
        FROM mongla_upazila;
    """
    # Note: 'geom' and 'name' are assumed column names. Modify if different.
    
    try:
        rows = await database.fetch_all(query=query)
    except Exception as e:
        print(f"DB Error: {e}") # Log to console
        raise HTTPException(status_code=500, detail=f"Database query failed: {str(e)}")
        
    features = []
    for row in rows:
        features.append({
            "type": "Feature",
            "geometry": json.loads(row["geometry"]),
            "properties": {
                "id": row["id"],
                "name": row["adm3_en"] if "adm3_en" in row else "Unknown"
            }
        })
        
    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/observations", response_model=ObservationFeatureCollection, tags=["GIS Data"], summary="Get iNaturalist Observations")
async def get_observations():
    """
    Get recent observations from iNaturalist as GeoJSON.
    
    Returns enriched data including **User**, **Quality Grade**, **Place**, and **Photos**.
    """
    url = "https://www.inaturalist.org/observations.json"
    params = {
        "per_page": 20, # Increased limit based on "provide me more data"
        "has[]": "geo"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as e:
            print(f"External API Error: {e}")
            raise HTTPException(status_code=502, detail=f"Failed to fetch data from iNaturalist: {str(e)}")

    features = []
    for obs in data:
        if obs.get("latitude") is None or obs.get("longitude") is None:
            continue
            
        species = obs.get("species_guess", "Unknown Species")
        place = obs.get("place_guess", "Unknown Location")
        observed_on = obs.get("observed_on", "")
        img_url = obs["photos"][0]["medium_url"] if obs.get("photos") else None
        
        features.append(
            ObservationFeature(
                geometry=GeoJSONPoint(
                    coordinates=[float(obs["longitude"]), float(obs["latitude"])]
                ),
                properties=ObservationProperties(
                    id=obs["id"],
                    species_guess=species,
                    user_login=obs.get("user_login", "unknown"), # Flattened in some API versions or inside 'user' dict
                    place_guess=place,
                    quality_grade=obs.get("quality_grade", "casual"),
                    observed_on=observed_on,
                    image_url=img_url,
                    description=obs.get("description")
                )
            )
        )

    return ObservationFeatureCollection(features=features)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
