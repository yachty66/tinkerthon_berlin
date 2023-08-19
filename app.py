from potassium import Potassium, Request, Response
import os
import leafmap
from samgeo import SamGeo, tms_to_geotiff, get_basemaps
from geopy.geocoders import Nominatim
import logging

logging.basicConfig(level=logging.INFO)

app = Potassium("bark")

@app.init
def init():
    logging.info("Initializing model...")
    model = SamGeo(
        model_type="vit_h",
        checkpoint="sam_vit_h_4b8939.pth",
        sam_kwargs=None,
    )
    context = {
        "model": model
    }
    logging.info("Model initialized.")
    return context

def generate_image(address):
    logging.info(f"Generating image for address: {address}")
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    m = leafmap.Map(center=[location.latitude, location.longitude], zoom=19)
    m.add_basemap("SATELLITE")
    if m.user_roi_bounds() is not None:
        bbox = m.user_roi_bounds()
    else:
        bbox = [location.longitude - 0.0024, location.latitude - 0.0008, location.longitude + 0.002, location.latitude + 0.0013]
    image = "satellite.tif"
    tms_to_geotiff(output=image, bbox=bbox, zoom=20, source="Satellite", overwrite=True)
    logging.info("Image generated.")
    return image, m 

@app.handler()
def handler(context: dict, request: Request) -> Response:
    logging.info("Handling request...")
    address = request.json.get("address")
    image, m = generate_image(address)
    model = context.get("model")
    mask = "segment.tif"
    model.generate(
        image, mask, batch=True, foreground=True, erosion_kernel=(3, 3), mask_multiplier=255
    )
    vector = "segment.gpkg"
    model.tiff_to_gpkg(mask, vector, simplify_tolerance=None)
    shapefile = "segment.shp"
    model.tiff_to_vector(mask, shapefile)
    style = {
        "color": "#3388ff",
        "weight": 2,
        "fillColor": "#7c4185",
        "fillOpacity": 0.5,
    }
    m.add_vector(vector, layer_name="Vector", style=style)
    m.to_html("map.html")
    with open("map.html", "r") as f:
        map_html = f.read()
    logging.info("Request handled.")
    return Response(json={"output": map_html}, status=200)

if __name__ == "__main__":
    logging.info("Starting server...")
    app.serve()