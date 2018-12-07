import numpy as np
import os
from osgeo import gdal,osr
import copy
from PIL import Image
import time

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

"""Function for subtracting getting a change mask of two images by subtracting corresponding pixel values and seting them in a new 2D array.

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
                #We are only interested in the change, not wether or not the change is positive or negative
                sub[px,py] = abs(image1[px][py] - image2[px][py]) 
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

def CreateGeoTiff(path,result, driver, xsize, ysize, GeoT, Projection, DataType, thresholdLimit):
    print("-- Creating GeoTiff --")
    #if DataType == 'Float32':
    DataType = gdal.GDT_Float32
    filename = "B08_RESULT_T_"+str(thresholdLimit)+".tif"
    NewFileName = os.path.join(path,filename)

    #checks if result directory exists and creates it if not
    if not os.path.exists(path):
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
        print("file" + NewFileName + " already exists")

"""Function for creating a new .Tif file.

:param sub:             2D array with calculated pixel differences
:param originalTif:     Unprocessed .tif file, read via gdal.Open(). Used for getting all geo data
:returns: 2D Array with calculated pixel differences
"""
def createTif(sub, originalTif, thresholdLimit, resultpath):
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    result = sub
    xsize, ysize, GeoT, Projection, DataType = GetGeoInfo(originalTif)
    newFile = CreateGeoTiff(resultpath,result,driver,xsize,ysize,GeoT,Projection,DataType,thresholdLimit)
    return newFile

"""Function for thresholding a 2D array.

:param array:       2D array with calculated pixel differences
:returns: 2D Array with thresholded pixel differences
"""
def treshold(array, thresholdLimit):
    result = (array > thresholdLimit) * array
    """
    TODO:
        Find a good threshold value !!
    """
    return result



start_time = time.time()

cwd = os.getcwd()
filepath = os.path.join(cwd,'tifs')
resultpath = os.path.join(cwd,'result')
arr = os.listdir(filepath)
print(arr)
thresholdLimit = 500
tifArrays = []
originalTif = gdal.Open(os.path.join(filepath, arr[0]), gdal.GA_ReadOnly)

for image in arr:
    tifArray = loadTifAsArray(image, filepath)
    tifArrays.append(tifArray)
print("--- %s seconds for loading the images ---" % (time.time() - start_time))

sub = subtract(tifArrays[0], tifArrays[1])
print("--- %s seconds for loading and subtracting ---" % (time.time() - start_time))

subTresh = treshold(sub, thresholdLimit)

print("--- %s seconds for loading, subtracting and tresholding ---" % (time.time() - start_time))

newTif = createTif(subTresh, originalTif, thresholdLimit, resultpath)
print("--- %s seconds for everything ---" % (time.time() - start_time))

