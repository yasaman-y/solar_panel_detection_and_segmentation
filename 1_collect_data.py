import os
from sys import path

from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")
import logging

import folium
path.append(os.path.join(os.getcwd(), '')) 
os.chdir(os.path.join(os.getcwd(), ''))

from utils.functions import *
from utils.functions_satellite_image import *

#=================================================================================================================================================

'''Authenticate and initialize'''
#=======================
# Load environment variables from .env file
load_dotenv()

# # Load Earth Engine private key file from environment variable
# ee_private_key_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# # Initialize Earth Engine API with service account private key
# credentials = ee.ServiceAccountCredentials(None, ee_private_key_file)
# ee.Initialize(credentials)

# # Trigger the authentication flow.
# ee.Authenticate()
# # Initialize the library.
# ee.Initialize()    


GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")

credentials = ee.ServiceAccountCredentials(SERVICE_ACCOUNT, GOOGLE_APPLICATION_CREDENTIALS)
ee.Initialize(credentials)

print("Earth Engine initialized")


#=================================================================================================================================================

'''Test the API'''

#=======================

# Print the elevation of Mount Everest.
dem = ee.Image('USGS/SRTMGL1_003')
xy = ee.Geometry.Point([86.9250, 27.9881])
elev = dem.sample(xy, 30).first().get('elevation').getInfo()
print('Mount Everest elevation (m):', elev)

#=================================================================================================================================================

"""Layer for folium"""

#=======================

# Add custom basemaps to folium
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Maps',
        overlay = True,
        control = True
    ),
    'Google Satellite': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Google Terrain': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Terrain',
        overlay = True,
        control = True
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Google Satellite',
        overlay = True,
        control = True
    ),
    'Esri Satellite': folium.TileLayer(
        tiles = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr = 'Esri',
        name = 'Esri Satellite',
        overlay = True,
        control = True
    )
}

#=================================================================================================================================================

"""Test ploting some Polygon for collect image"""

#=======================

# Opening a GeoJSON file
with open('data/geojason/selected_polygon.geojson') as f:
    data = json.load(f)

geometry = data['features'][0]['geometry']["geometries"][1]["coordinates"]
polygon = ee.Geometry.Polygon(geometry)


# Define map center and zoom level
centroid = geometry[0][0]
map_center = [centroid[1], centroid[0]] 
zoom_level = 100


# Create a folium map object.
my_map = folium.Map(location=map_center, zoom_start=100)

# Add the polygon geometry to the map
folium.GeoJson(
    data=polygon.getInfo(),
    name='Polygon',
    style_function=lambda feature: {
        'fillColor': None,
        'color': 'red',
        'weight': 2
    }
).add_to(my_map)

# Add custom basemaps
basemaps['Google Maps'].add_to(my_map)
basemaps['Google Satellite Hybrid'].add_to(my_map)
# display(my_map)
my_map.save("data/map.html")

#=================================================================================================================================================

"""Get image from google map from saved geojson file (test)"""

#=======================

path = 'data/google_map'
#test to get some polygon
geometry = {'coordinates': [[[-94.57260260212433, 39.14019525724463],
       [-94.57071164476883, 39.14019525724463],
       [-94.57071164476883, 39.141118918340055],
       [-94.57260260212433, 39.141118918340055],
       [-94.57260260212433, 39.14019525724463]]],
     'type': 'Polygon'}
zoom = 22
download_im(path, geometry, zoom)

#=================================================================================================================================================

# edite multipolygon geojson to polygons
# list_files = os.listdir("data/geojason") 
list_files = ["geometry_limon.geojson"]


l = []
list_of_poly = []

for file_ in list_files:
  flag = -1
  print(file_)
  with open(f'data/geojason/{file_}') as f:
    data = json.load(f)
    l.append(data)

  try:
    x = data["features"][0]["geometry"]["coordinates"][0]
    flag = 1
  except Exception as er:
    flag = 0
    continue

  if flag == 0:
    x = data['features'][0]['geometry']["geometries"][1]["coordinates"]
    list_of_poly.append(x)


  if flag == 1:
    x = data["features"][0]["geometry"]["coordinates"]
    print(len(x))
    for i in range(0,len(x)):
      dic_0 = {
          'coordinates': data["features"][0]["geometry"]["coordinates"][i],
          'type': 'Polygon'
          }
      list_of_poly.append(dic_0)

# print(len(l))
path_ = "data/google_map"
for poly in list_of_poly:
  zoom = 19
  download_im(path_,poly, zoom)


#=================================================================================================================================================
  
"""splite large image"""

#=======================

#for splite those images from polygon to small size
list_files = os.listdir("data/google_map/") 

for file_ in list_files:
    path = "data/splited_image"
    # input = "data/google_map_figures/" + file_
    input = "data/google_map/" + file_

    # dir_in =  "data/google_map_figures/"
    dir_in =  "data/google_map/"


    # crop_2(path, input)
    tile(file_, dir_in, path, 500)