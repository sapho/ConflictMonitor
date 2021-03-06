import os
from os import listdir
from os.path import isfile, join

import subprocess
from osgeo import gdal
from osgeo import osr
import time


tifInputDir = '/data/nbr/'
layerOutputDir = '/data/output/nbr/'

def getfiles():
    onlyfiles = [f for f in listdir(tifInputDir) if isfile(join(tifInputDir, f))]
    return onlyfiles

fileList = getfiles()

gdalTilesBase = ["gdal2tiles.py", "-w", "leaflet"]

for imgFile in fileList:
    if imgFile.endswith(".tif"):
        sourcepath = os.path.join(tifInputDir, imgFile)
        outputpath = os.path.join(layerOutputDir, imgFile).replace('.tif','')
        gdalTiles = gdalTilesBase + [sourcepath, outputpath]
        subprocess.call(gdalTiles)