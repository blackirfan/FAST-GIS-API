from models import PersonalInfo, LocationFeature, LocationProperties, GeoJSONPoint, GeoJSONPolygon, LocationFeatureCollection

personal_info = PersonalInfo(
    name="John Doe",
    role="Full Stack GIS Developer",
    bio="Passionate about building spatial applications and connecting people with places.",
    contact_email="john.doe@example.com"
)

# Sample locations
locations = [
    LocationFeature(
        geometry=GeoJSONPoint(coordinates=[-74.0060, 40.7128]), # NYC
        properties=LocationProperties(
            name="New York Office",
            description="Our main headquarters.",
            category="Work"
        )
    ),
    LocationFeature(
        geometry=GeoJSONPoint(coordinates=[-0.1276, 51.5074]), # London
        properties=LocationProperties(
            name="London Branch",
            description="European GIS hub.",
            category="Work"
        )
    ),
     LocationFeature(
        geometry=GeoJSONPoint(coordinates=[-122.4194, 37.7749]), # SF
        properties=LocationProperties(
            name="San Francisco Home",
            description="Where I live.",
            category="Home"
        )
    )
]

# Sample Zones (Polygons)
zones = [
    LocationFeature(
        geometry=GeoJSONPolygon(
            coordinates=[[
                [-74.02, 40.70],
                [-74.02, 40.72],
                [-73.98, 40.72],
                [-73.98, 40.70],
                [-74.02, 40.70]
            ]]
        ),
        properties=LocationProperties(
            name="Downtown Zone",
            description="Business district area.",
            category="Zone"
        )
    ),
    LocationFeature(
        geometry=GeoJSONPolygon(
            coordinates=[[
                [-0.142, 51.501],
                [-0.142, 51.504],
                [-0.138, 51.504],
                [-0.138, 51.501],
                [-0.142, 51.501]
            ]]
        ),
        properties=LocationProperties(
            name="Hyde Park Corner",
            description="Green space in London.",
            category="Park"
        )
    ),
     LocationFeature(
        geometry=GeoJSONPolygon(
            coordinates=[[
                [-122.42, 37.77],
                [-122.42, 37.79],
                [-122.40, 37.79],
                [-122.40, 37.77],
                [-122.42, 37.77]
            ]]
        ),
        properties=LocationProperties(
            name="Bay Area Tech Hub",
            description="Innovation zone.",
            category="Zone"
        )
    )
]

location_collection = LocationFeatureCollection(features=locations)
zone_collection = LocationFeatureCollection(features=zones)
