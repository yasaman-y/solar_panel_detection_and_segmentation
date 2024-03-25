
# import seaborn as sns
# from matplotlib.patches import Rectangle
# import matplotlib.pyplot as plt
# # from skimage.io import imread
# from matplotlib.collections import PatchCollection
# from matplotlib.patches import Rectangle
# import cv2

# from fastai.vision import *
# from IPython.core.display import HTML
# HTML("<style>div.output_area pre {white-space: pre;}</style>")
# import ipywidgets as widgets
# from IPython.display import display
# %matplotlib inline
# print("ee v",ee.__version__)

# import geopandas as gpd
# import matplotlib.pyplot as plt
# import folium
# from folium import plugins
# import sentinelhub
# import gpd
# from geopandas import GeoSeries, GeoDataFrame

# import georaster
# import geemap


import pandas as pd
import numpy as np
import os
import json
from PIL import Image, ImageDraw

import json
import time 
import ee

from turfpy.measurement import bbox
import math
from PIL import Image
import requests
import os
from PIL import Image
from itertools import product



def num2deg(xtile, ytile, zoom):
    n = 2.0 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(lat_rad)
    return (lat_deg, lon_deg)


def getXY(lng, lat, zoom): 
    """takes longitude (lng), latitude (lat), and zoom level (zoom) as inputs and returns
      the X and Y tile coordinates for a specific point on a map using the Mercator projection"""
    tile_size = 256
    numTiles = 1 << zoom
    point_x = (tile_size/ 2 + lng * tile_size / 360.0) * numTiles // tile_size
    sin_y = math.sin(lat * (math.pi / 180.0))
    point_y = ((tile_size / 2) + 0.5 * math.log((1+sin_y)/(1-sin_y)) * -(tile_size / (2 * math.pi))) * numTiles // tile_size
    return int(point_x), int(point_y)


def download_im(path,geometry, zoom):
    """downloads map tiles from Google Maps and stitches them together to create a larger map image based on a given bounding box (bbox)."""
    num = 0
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'}
    minlon, minlat, maxlon, maxlat = bbox(geometry)  #change an polygon to a rectangle area
    print(minlon, minlat, maxlon, maxlat)

    start_x, start_y = getXY(minlon, maxlat, zoom)
    end_x, end_y = getXY(maxlon, minlat, zoom)


    start_x -=1
    start_y -=1

    end_x +=1
    end_y +=1


    w = (end_x+1 - start_x) * 256
    h = (end_y+1 - start_y) * 256
    result = Image.new("RGB", (w, h))

    for x in range(start_x, end_x+1):
        for y in range(start_y, end_y+1):
            print(f"donwloading {num}/{((end_x+1) - (start_x)) * ((end_y+1) - (start_y)) }")
            
            while True:
                try:
                    url = "http://mt1.google.com/vt/lyrs=y&x={}&y={}&z={}".format(x,y, zoom)
                    raw = requests.get(url, stream=True, headers=header).raw
                    break
                except:
                    continue
            
            i = Image.open(raw)
            x_paste = (x - start_x) * 256
            y_paste = h - (end_y+1 - y) * 256
            result.paste(i, (x_paste, y_paste))
            num +=1
    name = os.path.join(path, "map_{}_{}_{}_{}.png".format(minlat, minlon, maxlat, maxlon))
    result.save(os.path.join (name))
    return result, start_x, start_y, end_x, end_y, w, h


def crop(path, input):
    k = 0

    im = Image.open(input)
    imgwidth, imgheight = im.size


    width = int(np.floor(imgwidth/5))
    height = int(np.floor(imgheight/5))

    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            try:
                # o = a.crop(area)
                a.save(os.path.join(path,"IMG-%s.png" % k))
            except Exception as er:
                print(er)
                pass
            k +=1


def crop_2(path, input):
    k = 0

    im = Image.open(input)
    imgwidth, imgheight = im.size

    W = 2
    H = 2

    width = int(np.floor(imgwidth/W))
    height = int(np.floor(imgheight/H))

    x_0 = 0
    y_0 = 0

    for i in range(0,W):
        for j in range(0,H):

            box = (x_0, y_0, x_0+width, y_0+height)
            x_0 = x_0+width
            y_0 =  y_0+height

            # im.crop((left, top, right, bottom))
            a = im.crop(box)  
            try:
                # o = a.crop(area)
                a.save(os.path.join(path,"IMG-%s.png" % k))
            except Exception as er:
                print(er)
                pass
            k +=1


def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

