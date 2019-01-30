import numpy as np
import os
from osgeo import gdal
from gdalconst import *
from osgeo import osr


def subset(filepath,image,size):
    print("in subset")
    subsetBandPath = os.path.join(filepath,image)
    subsetBand = gdal.Open(subsetBandPath)
    getBand = subsetBand.GetRasterBand(1)
    outFile = os.path.join(filepath,'subsets',image)
    result = gdal.Translate(outFile,subsetBandPath,format="GTiff",width=size,height=size,resampleAlg="nearest",outputType=gdal.GDT_Float32)

cwd = os.getcwd()
root = os.path.dirname(cwd)
filepath = os.path.join(root,'data','nbr')
arr = os.listdir(filepath)
arr.remove('bfastPlots')
arr.remove('subsets')
for image in arr:
    subset(filepath,image,100)
