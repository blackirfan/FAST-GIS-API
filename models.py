from pydantic import BaseModel, Field
from typing import List, Optional, Union

class GeoJSONPoint(BaseModel):
    type: str = Field("Point", description="GeoJSON geometry type")
    coordinates: List[float] = Field(..., description="[longitude, latitude]", examples=[[-74.0060, 40.7128]])

class GeoJSONPolygon(BaseModel):
    type: str = Field("Polygon", description="GeoJSON geometry type")
    coordinates: List[List[List[float]]] = Field(..., description="List of linear rings. First ring is exterior.", examples=[[[[-74.0, 40.0], [-74.0, 41.0], [-73.0, 41.0], [-73.0, 40.0], [-74.0, 40.0]]]])

class GeoJSONMultiPolygon(BaseModel):
    type: str = Field("MultiPolygon", description="GeoJSON geometry type")
    coordinates: List[List[List[List[float]]]] = Field(..., description="List of Polygons, which are lists of rings.", examples=[[[[[-74.0, 40.0], [-74.0, 41.0], [-73.0, 41.0], [-73.0, 40.0], [-74.0, 40.0]]]]])

class LocationProperties(BaseModel):
    name: str = Field(..., description="Name of the location", examples=["Central Park"])
    description: Optional[str] = Field(None, description="Short description of the location")
    category: str = Field(..., description="Category of the location", examples=["Park"])

class LocationFeature(BaseModel):
    type: str = Field("Feature", description="GeoJSON feature type")
    geometry: Union[GeoJSONPoint, GeoJSONPolygon, GeoJSONMultiPolygon]
    properties: LocationProperties

class LocationFeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="GeoJSON feature collection type")
    features: List[LocationFeature]

class MonglaProperties(BaseModel):
    id: int = Field(..., description="Unique ID from database")
    name: str = Field(..., description="Name of the administrative area (Upazila)", examples=["Mongla"])

class MonglaFeature(BaseModel):
    type: str = Field("Feature", description="GeoJSON feature type")
    geometry: Union[GeoJSONPoint, GeoJSONPolygon, GeoJSONMultiPolygon]
    properties: MonglaProperties

class MonglaFeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="GeoJSON feature collection type")
    features: List[MonglaFeature]

class MonglaFeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="GeoJSON feature collection type")
    features: List[MonglaFeature]

class ObservationProperties(BaseModel):
    id: int = Field(..., description="iNaturalist Observation ID")
    species_guess: Optional[str] = Field(None, description="Species name")
    user_login: Optional[str] = Field(None, description="Username of observer")
    place_guess: Optional[str] = Field(None, description="Location description")
    quality_grade: Optional[str] = Field(None, description="Quality grade (casual, research, needs_id)")
    observed_on: Optional[str] = Field(None, description="Date of observation")
    image_url: Optional[str] = Field(None, description="URL of the photo")
    description: Optional[str] = Field(None, description="Description")

class ObservationFeature(BaseModel):
    type: str = Field("Feature", description="GeoJSON feature type")
    geometry: GeoJSONPoint
    properties: ObservationProperties

class ObservationFeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="GeoJSON feature collection type")
    features: List[ObservationFeature]

class PersonalInfo(BaseModel):
    name: str = Field(..., description="Full name of the developer", examples=["Jane Doe"])
    role: str = Field(..., description="Current job title or role", examples=["Senior GIS Developer"])
    bio: str = Field(..., description="Short biography", examples=["Loves maps and code."])
    contact_email: str = Field(..., description="Contact email address", examples=["jane@example.com"])

class BangladeshProperties(BaseModel):
    id: int = Field(..., description="Unique ID from database")
    shapename: str = Field(..., description="District Name")
    shapeiso: Optional[str] = Field(None, description="ISO Code")
    shapeid: Optional[str] = Field(None, description="Shape ID")
    shapegroup: Optional[str] = Field(None, description="Shape Group")
    shapetype: Optional[str] = Field(None, description="Shape Type")

class BangladeshFeature(BaseModel):
    type: str = Field("Feature", description="GeoJSON feature type")
    geometry: Union[GeoJSONPoint, GeoJSONPolygon, GeoJSONMultiPolygon]
    properties: BangladeshProperties

class BangladeshFeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", description="GeoJSON feature collection type")
    features: List[BangladeshFeature]
