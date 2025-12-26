import asyncio
import json
import sys
from db import database

async def check_stats():
    await database.connect()
    try:
        # Check Bangladesh Level Two
        count_query = "SELECT count(*) FROM bangladesh_level_two;"
        size_query = "SELECT avg(length(ST_AsGeoJSON(geom))) FROM bangladesh_level_two;"
        
        count = await database.fetch_one(query=count_query)
        avg_size = await database.fetch_one(query=size_query)
        
        print(f"Table: bangladesh_level_two")
        print(f"  Count: {count[0]}")
        print(f"  Avg Geometry Size (Chars): {avg_size[0]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(check_stats())
