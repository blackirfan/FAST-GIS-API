import os
import databases
from sqlalchemy import create_engine, MetaData

# Default to creating a local connection if env var not set
# Assuming default postgres credentials for local dev as requested
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:123321@localhost:5432/demo_webgis"
)
database = databases.Database(DATABASE_URL)
