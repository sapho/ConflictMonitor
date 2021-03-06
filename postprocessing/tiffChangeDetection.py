#!/usr/bin/python3
import os
import time
import copy
import numpy as np
import cv2
from osgeo import gdal,osr
from PIL import Image
from scipy.ndimage import median_filter
import sys
cwd = os.getcwd()
cwdEnd = cwd[len(cwd)-7:]
if cwdEnd != 'scripts':
    sys.path.append('conflicMonitoring/postprocessing/scripts')
    print(sys.path)
    import utils_hist
else:
    import utils_hist

"""Function for loading a .tif file as an array.
:param image:       Name of the .tif file to be loaded.
:param filepath:    Path to the tifs directory
:returns: 2D Array with .tif pixel values.
"""
def loadTifAsArray(imgPath):
    print("Loading "+imgPath)
    path = imgPath
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
    result = utils_hist.hist_match(source, template)
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

def CreateGeoTiff(path,result, driver, xsize, ysize, GeoT, Projection, DataType, nClusters, resultname):

    print("-- Creating GeoTiff --")
    #if DataType == 'Float32':
    DataType = gdal.GDT_Float32
    filename = resultname+".tif"
 
    NewFileName = os.path.join(path,filename)

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
def createTif(sub, originalTif, nClusters, resultpath, resultname):
    print("resultname:" + resultname)
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    result = sub
    xsize, ysize, GeoT, Projection, DataType = GetGeoInfo(originalTif)
    newFile = CreateGeoTiff(resultpath,result,driver,xsize,ysize,GeoT,Projection,DataType,nClusters, resultname)
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
    Z[np.isnan(Z)]

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret,label,center=cv2.kmeans(Z,clusters,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Define limit for tresholding
    print(np.sort(center))
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


"""Function for triggering the change detection
"""
def tiffChangeDetection(imgPath1, imgPath2, name):
    nClusters = 6       #number of clusters 
    clusterLimit = 3    #top x clusters to not be removed when tresholding
    filterLimit = 5     #Filtering neighborhood 
    originalTif = gdal.Open(imgPath1, gdal.GA_ReadOnly)
    resultpath = "~/data/change"
    
    #resultname = imgPath1[11:19]+"_"+imgPath1[38:44]+"_" + imgPath2[11:19]+"_"+imgPath2[38:44]
    resultname = name
    
    img1 = loadTifAsArray(imgPath1)
    img2 = loadTifAsArray(imgPath2)

    matched = hist_matching(img1, img2)
    img1 = matched

    sub = subtract(img1, img2)

    subTresh = treshold(sub, nClusters, clusterLimit)

    subFiltered = filter(subTresh, filterLimit)

    newTif = createTif(subFiltered, originalTif, nClusters, resultpath, resultname)

    return newTif


def readPath(image):
    print("in readPath")
    datum = image[11:27]
    name = image[38:45]
    nameDatum = name + datum
    return nameDatum

def readBand(filepath,image,resolution,nameDatum,band):
    print("in readBand")
    band = os.path.join(filepath,image,'IMG_DATA',resolution, nameDatum + band + '.tif')
    if((os.path.isfile(band))):
        open_band = gdal.Open(band)
        img = open_band.ReadAsArray()
        img_float = img.astype(float)
        return img_float
    else:
        print("file"+ band + " not exists")

def callTiffChangeDetection(bDict,filepath,resolution):
    print("in nbrOldNew")
    for key in bDict:
        if(key != len(bDict)):
            oldPath = os.path.join(filepath,bDict[key][1],'IMG_DATA',resolution,bDict[key][0])
            newPath = os.path.join(filepath,bDict[key+1][1],'IMG_DATA',resolution,bDict[key+1][0])
            nameDatum = readPath(bDict[key][1])
            nameDatum2 = readPath(bDict[key+1][1])
            outChangeDetect = nameDatum + nameDatum2 + "B08_ChangeDetection"
            tiffChangeDetection(oldPath,newPath,outChangeDetect)
        else:
            print("All changes computed")

def datumCharsB(x):
    return(x[7:15])

def datumCharsArr(x):
    return(x[11:19])

cwd = os.getcwd()
root = os.path.dirname(cwd)
filepath = os.path.join(root,'data','input')
arr = os.listdir(filepath)
bArray = []

for image in arr:
    path = readPath(image)
    nir = readBand(filepath,image,"R10m",path,"B08_10m")
    if(np.all(nir) is not None):
        join = path+"B08_10m.tif"
        bArray.append(join)

sortedB = sorted(bArray, key = datumCharsB)
sortedArr = sorted(arr, key = datumCharsArr)

bDict = {}
counter = 1
for b, path in zip(sortedB,sortedArr):
    bDict[counter] = (b,path)
    counter += 1

callTiffChangeDetection(bDict,filepath,resolution)
