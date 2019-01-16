#!/usr/bin/python3
import os
import time
import copy
import numpy as np
import cv2
from osgeo import gdal,osr
from PIL import Image
from scipy.ndimage import median_filter
import utils

"""Function for loading a .tif file as an array.
:param image:       Name of the .tif file to be loaded.
:param filepath:    Path to the tifs directory
:returns: 2D Array with .tif pixel values.
"""
def loadTifAsArray(image, filepath):
    print("Loading "+image)
    path = os.path.join(filepath,image)
    img = gdal.Open(path) 
    tifArray = img.ReadAsArray()
    return tifArray

"""Function for normalizing 2 images by histogram matching 
:param array:       2D array 
:param array:       2D array 

:returns: 2D Source 2D array, with histo-matched pixel values
"""
def hist_matching(img1, img2):
    print("Histogram-matching...") 
    source = img1
    template = img2
    result = utils.hist_match(source, template)
    return result

"""Function for getting a change mask of two images by subtracting corresponding pixel values and seting them in a new 2D array.
:param image1:      Array with pixelvalues of the first .tif
:param image2:      Array with pixelvalues of the second .tif
:returns: 2D Array with calculated pixel differences
"""
def subtract(image1, image2):
    # Copy of one of the images is used for saving calculated values
    print("Subtracting ...")
    #Cast to float32 because in uint16 images, negative numbers "wrap around" back to the maximal value.
    image1 = np.array(image1).astype(np.float32)
    image2 = np.array(image2).astype(np.float32)

    if image1.shape == image2.shape : 
        sub = copy.deepcopy(image1)
        rows = len(sub)    
        cols = len(sub[0])
        for px in range(cols):
            for py in range(rows):
                #subtraction, normalized by dividing the subtraction of two pixel values by the sum of both pixel values
                sub[px,py] = (abs(image1[px][py] - image2[px][py])) / (image1[px][py] + image2[px][py])
        return sub
    else:
        print("Images don't have the same dimensions")


def GetGeoInfo(originalTif):
    print("-- GeoInfo --")
    SourceDS = originalTif
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    DataType = SourceDS.GetRasterBand(1).DataType
    DataType = gdal.GetDataTypeName(DataType)
    return xsize, ysize, GeoT, Projection, DataType

def CreateGeoTiff(path,result, driver, xsize, ysize, GeoT, Projection, DataType, nClusters):

    print("-- Creating GeoTiff --")
    #if DataType == 'Float32':
    DataType = gdal.GDT_Float32
    filename = "B08_RESULT_T_"+str(nClusters)+"clusters.tif"
    NewFileName = os.path.join(path,filename)

    #checks if result directory exists and creates it if not
    if not os.path.exists(path):
        print("Creating Result directory...")
        os.makedirs(path)

    #checks if file already exists
    if(not(os.path.isfile(NewFileName))):
        # Set up the dataset
        DataSet = driver.Create(NewFileName, xsize, ysize, 1, DataType) # the '1' is for band 1.
        DataSet.SetGeoTransform(GeoT)
        DataSet.SetProjection(Projection.ExportToWkt())
        # Write the array
        DataSet.GetRasterBand(1).WriteArray(result)
        DataSet.FlushCache()
        print("new dataset created")
        return NewFileName
    else:
        print("#ERROR: file" + NewFileName + " already exists")

"""Function for creating a new .Tif file.
:param sub:             2D array with calculated pixel differences
:param originalTif:     Unprocessed .tif file, read via gdal.Open(). Used for getting all geo data
:returns: 2D Array with calculated pixel differences
"""
def createTif(sub, originalTif, nClusters, resultpath):
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    result = sub
    xsize, ysize, GeoT, Projection, DataType = GetGeoInfo(originalTif)
    newFile = CreateGeoTiff(resultpath,result,driver,xsize,ysize,GeoT,Projection,DataType,nClusters)
    return newFile

"""Function for calculating a tresholdlimit via k-means
:param array:       2D array with calculated pixel differences
:returns: treshold limit
"""
def kMeansLimit(sub, clusters, clusterLimit ):
    print("K-Means with "+ str(clusters) +" clusters...")
    x = sub.reshape((-1,1))
    # convert to np.float32
    Z = np.float32(x)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans(Z,clusters,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Define limit for tresholding
    print(np.sort(center))
    print(np.sort(center)[clusterLimit])
    limitCenter = np.sort(center)[clusterLimit-1][0] * 1.25  #+ 25% above the center to catch more outliers
    return limitCenter

"""Function for thresholding a 2D array.
:param array:       2D array with calculated pixel differences
:returns: 2D Array with thresholded pixel differences
"""
def treshold(sub, clusters, clusterLimit):
    print("Tresholding...")
    limitCenter = kMeansLimit(sub, clusters, clusterLimit)
    print(limitCenter)
    result = (sub > limitCenter) * sub
    return result

"""Function for applying a meadian filter on an image
:param array:       2D array with calculated pixel differences, already applied trashold
:returns: 2D Array with filtered outliers via median filter
"""
def filter(array, limit):
    print("Median-Filter...")
    filteredImg = np.array(median_filter(array, size=limit)).astype(np.float32)
    return filteredImg


start_time = time.time()

cwd = os.getcwd()
filepath = os.path.join(cwd,'tifs')
resultpath = os.path.join(cwd,'result')
arr = os.listdir(filepath)
print(arr)
nClusters = 6       #number of clusters 
clusterLimit = 3    #top x clusters to not be removed when tresholding
filterLimit = 5     #Filtering neighborhood 
tifArrays = []
originalTif = gdal.Open(os.path.join(filepath, arr[0]), gdal.GA_ReadOnly)

for image in arr:
    tifArray = loadTifAsArray(image, filepath)
    tifArrays.append(tifArray)
print("--- %s seconds for loading the images ---" % (time.time() - start_time))

matched = hist_matching(tifArrays[0], tifArrays[1])
tifArrays[0] = matched
print("--- %s seconds for loading the images & histogram matching ---" % (time.time() - start_time))

sub = subtract(tifArrays[0], tifArrays[1])
print("--- %s seconds for loading the images & histogram matching & subtracting ---" % (time.time() - start_time))

subTresh = treshold(sub, nClusters, clusterLimit)
print("--- %s seconds for loading the images & histogram matching & subtracting & tresholding with k-means clustering  ---" % (time.time() - start_time))

subFiltered = filter(subTresh, filterLimit)
print("--- %s seconds everything previous + filtering ---" % (time.time() - start_time))

newTif = createTif(subFiltered, originalTif, nClusters, resultpath)
print("--- %s seconds for everything ---" % (time.time() - start_time))