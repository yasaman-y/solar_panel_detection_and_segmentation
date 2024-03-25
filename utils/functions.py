
# import pandas as pd
# import numpy as np
# import json
# import os
# import seaborn as sns
# from matplotlib.patches import Rectangle
# import json
# import pandas as pd
# import matplotlib.pyplot as plt
# # from skimage.io import imread
# from matplotlib.collections import PatchCollection
# from matplotlib.patches import Rectangle
# from PIL import Image, ImageDraw
# import cv2

# from fastai.vision import *
# from IPython.core.display import HTML
# HTML("<style>div.output_area pre {white-space: pre;}</style>")
# import ipywidgets as widgets
# from IPython.display import display
# # %matplotlib inline
# import ee
# # print("ee v",ee.__version__)

# # import geopandas as gpd
# import matplotlib.pyplot as plt
# import folium
# from folium import plugins
# # import sentinelhub
# # import gpd
# # from geopandas import GeoSeries, GeoDataFrame
# import json
# import time 
# import georaster
# import geemap

# from turfpy.measurement import bbox
# import math
# from PIL import Image
# # import requests

# import os
# import numpy as np
# from PIL import Image
# from itertools import product



def replace_name_of_categori(x):
  if x == 0:
    return 'roof-panel'
  if x ==1 :
    return 'panel'
  if x ==2:
    return 'roof'
  

def calculate_aspect_ratios(annotations):
    aspect_ratios = []

    for annotation in annotations:
        # Assuming annotation is in the format [x, y, width, height]
        width = annotation[2]
        height = annotation[3]
        aspect_ratio = float(width) / height
        aspect_ratios.append(aspect_ratio)

    return aspect_ratios