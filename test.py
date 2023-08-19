import os
import leafmap
from samgeo import tms_to_geotiff
from geopy.geocoders import Nominatim

#get längen und breitengrad von bestimmter hausnummer - return error address if not found 
def get_lat_long(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    m = leafmap.Map(center=[location.latitude, location.longitude], zoom=19)
    m.add_basemap("SATELLITE")
    #m
    return m
    #return location.latitude, location.longitude


address = "Schönhauser Allee 143"
lat, long = get_lat_long(address)
print(lat, long)


#get map image zoomed out by factor x  
"""def get_map_image(lat, long, zoom):
    pass


#input model into SAM and get back a segmented image
def get_segmented_image(image):
    #this going to be implemented on banana
    pass

#i think for being realistic about having a demo it would be enough to have the streetname as input and than the model returns an image with buildings segmented 

m = leafmap.Map(center=[29.676840, -95.369222], zoom=19)
m.add_basemap("SATELLITE")
m

if m.user_roi_bounds() is not None:
    bbox = m.user_roi_bounds()
else:
    bbox = [-95.3704, 29.6762, -95.368, 29.6775]

image = "satellite.tif"

tms_to_geotiff(output=image, bbox=bbox, zoom=20, source="Satellite", overwrite=True)

m.layers[-1].visible = False  # turn off the basemap
m.add_raster(image, layer_name="Image")
m
#what i want to do is to send an image to the api endpoint and than the endpoint should return me the segmented image 
#input of the model would be"""

