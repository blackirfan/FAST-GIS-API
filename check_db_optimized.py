import asyncio
from db import database

async def check_stats():
    await database.connect()
    try:
        # Check simplified Bangladesh Level Two
        size_query = "SELECT avg(length(ST_AsGeoJSON(ST_SimplifyPreserveTopology(geom, 0.001)))) FROM bangladesh_level_two;"
        avg_size = await database.fetch_one(query=size_query)
        
        print(f"Table: bangladesh_level_two (Optimized)")
        print(f"  Avg Simplified Geometry Size (Chars): {avg_size[0]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await database.disconnect()

if __name__ == "__main__":
    asyncio.run(check_stats())
