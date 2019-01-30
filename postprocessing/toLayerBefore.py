import os
from os import listdir
from os.path import isfile, join

import subprocess
from osgeo import gdal
from osgeo import osr

jp2InputDir = '/data/input/'
layerOutputDir = '/data/output/before/'

def getfiles():
    onlyfiles = [f for f in listdir(jp2InputDir) if isfile(join(jp2InputDir, f))]
    return onlyfiles

fileList = getfiles()

gdalTilesBase = ["gdal2tiles.py", "-w", "leaflet"]

for imgFile in fileList:
    if imgFile.endswith(".jp2") and 'TCI' in imgFile:
        sourcepath = os.path.join(jp2InputDir, imgFile)
        outputpath = os.path.join(layerOutputDir, imgFile).replace('.jp2','')
        gdalTiles = gdalTilesBase + [sourcepath, outputpath]
        subprocess.call(gdalTiles)