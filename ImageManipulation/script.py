# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt

# #GRAYSCALE ONLY FOR TESTING
# #Test with person appearing in image
# img1 = cv.imread("images/1.jpg", 0)
# img2 = cv.imread("images/2.jpg", 0)
# img3 = cv.subtract(img1, img2)
# ret, thresh1 = cv.threshold(img3, 0, 255, cv.THRESH_TOZERO)


# #Test with satelite image of japan landslide changes after earthquake
# jl_before = cv.imread("images/japan_earthquake_before.jpg",0)
# jl_after = cv.imread("images/japan_earthquake_after.jpg",0)
# jl_subtraction = cv.subtract(jl_after, jl_before)
# ts,thresh2 = cv.threshold(jl_subtraction,0,255,cv.THRESH_TOZERO)

# images = [img1, img2,img3 , thresh1, jl_before, jl_after,jl_subtraction, thresh2]
# titles = ["Image1", "Image2","Subtraction", "+ Treshold", "Japan_Before", "Japan_After","Subtraction", "+ Treshold" ]
# for i in range(8):
#     plt.subplot(2,4,i+1),plt.imshow(images[i],'gray')
#     plt.title(titles[i])
#     plt.xticks([]),plt.yticks([])
# plt.show()

import numpy as np
import os
from osgeo import gdal,osr
import copy
from PIL import Image
import time

def loadTifAsArray(image, filepath):
    print("Loading "+image)
    path = os.path.join(filepath,image)
    img = gdal.Open(path)
    tifArray = img.ReadAsArray()

    return tifArray

def subtract(image1, image2):
    # Copy of one of the images is used for saving calculated values
    print("Subtracting ...")
    #Cast to float32 because in uint16 images, negative numbers "wrap around" back to the maximal value.
    image1 = np.array(image1).astype(np.float32)
    image2 = np.array(image2).astype(np.float32)
    sub = copy.deepcopy(image1)
    rows = len(sub)    
    cols = len(sub[0])

    for px in range(cols):
        for py in range(rows):
            #We are only interested in the change, not wether or not the change is positive or negative
            sub[px][py] = abs(image1[px][py] - image2[px][py]) 
    print("sub min and max values:")
    print(sub.min())
    print(sub.max())
    return sub

def GetGeoInfo(originalTif):
    print("in getgeoinfo")
    SourceDS = originalTif
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    DataType = SourceDS.GetRasterBand(1).DataType
    DataType = gdal.GetDataTypeName(DataType)
    return xsize, ysize, GeoT, Projection, DataType

def CreateGeoTiff(array, driver, xsize, ysize, GeoT, Projection, DataType):
    print("in creategeotiff")
    #if DataType == 'Float32':
    print(array)
    DataType = gdal.GDT_Float32
    NewFileName = "B08_RESUUULT_25.tif"
    if(not(os.path.isfile(NewFileName))):
        # Set up the dataset
        DataSet = driver.Create(NewFileName, xsize, ysize, 1, DataType) # the '1' is for band 1.
        DataSet.SetGeoTransform(GeoT)
        DataSet.SetProjection(Projection.ExportToWkt())
        # Write the array
        DataSet.GetRasterBand(1).WriteArray(array)
        DataSet.FlushCache()
        print("new dataset created")
        return NewFileName
    else:
        print("file" + NewFileName + " already exists")


def createTif(sub, originalTif):
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    result = sub
    xsize, ysize, GeoT, Projection, DataType = GetGeoInfo(originalTif)
    newFile = CreateGeoTiff(result,driver,xsize,ysize,GeoT,Projection,DataType)


def treshold(array):
    result = array[array >= 25] = 0
    return result;


start_time = time.time()

cwd = os.getcwd()
filepath = os.path.join(cwd,'tifs')
arr = os.listdir(filepath)
print(arr)
tifArrays = []
originalTif = gdal.Open(os.path.join(filepath, arr[0]), gdal.GA_ReadOnly)

for image in arr:
    tifArray = loadTifAsArray(image, filepath)
    tifArrays.append(tifArray)

print("--- %s seconds for loading the images ---" % (time.time() - start_time))

sub = subtract(tifArrays[0], tifArrays[1])
print("--- %s seconds for loading and subtracting ---" % (time.time() - start_time))

subTresh = treshold(sub)
print("--- %s seconds for loading, subtracting and tresholding ---" % (time.time() - start_time))

createTif(subTresh, originalTif)
#print("--- %s seconds for everything ---" % (time.time() - start_time))

