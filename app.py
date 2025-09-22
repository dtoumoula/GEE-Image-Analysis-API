from fastapi import FastAPI
import ee

# Initialisation de l'application
app = FastAPI(title="GEE Image Analysis API")

# Authentification GEE
ee.Initialize()

@app.get("/")
def root():
    return {"message": "Bienvenue sur l'API GEE pour l'analyse d'images satellites."}

@app.get("/ndvi")
def compute_ndvi(lat: float, lon: float):
    """Exemple : calcul NDVI sur une zone."""
    point = ee.Geometry.Point([lon, lat])
    collection = ee.ImageCollection("COPERNICUS/S2") \
        .filterBounds(point) \
        .filterDate("2022-01-01", "2022-12-31") \
        .first()

    ndvi = collection.normalizedDifference(["B8", "B4"]).rename("NDVI")
    mean_dict = ndvi.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=point.buffer(500),
        scale=10
    ).getInfo()

    return {"lat": lat, "lon": lon, "NDVI": mean_dict.get("NDVI")}
