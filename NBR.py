import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from osgeo import gdal
import fnmatch
from gdalconst import *
from osgeo import osr

def resample(filepath,image,name_datum):
    print("in resample")
    resampleBandPath = os.path.join(filepath,image,"IMG_DATA",name_datum + "B12.tif")
    resampleBand = gdal.Open(resampleBandPath)
    getBand = resampleBand.GetRasterBand(1)
    outFile = os.path.join(filepath, image,"IMG_DATA",name_datum + "resampleB12.tif")
    if(not(os.path.isfile(outFile))):
        result = gdal.Translate(outFile,resampleBandPath,format="GTiff",width=10980,height=10980,resampleAlg="nearest",outputType=gdal.GDT_Float32)
        print("resampled an image")
    else:
        print("image" + outFile + " exists already")

# Function to read the original file's projection:
def GetGeoInfo(FileName):
    print("in getgeoinfo")
    SourceDS = gdal.Open(FileName, GA_ReadOnly)
    xsize = SourceDS.RasterXSize
    ysize = SourceDS.RasterYSize
    GeoT = SourceDS.GetGeoTransform()
    Projection = osr.SpatialReference()
    Projection.ImportFromWkt(SourceDS.GetProjectionRef())
    DataType = SourceDS.GetRasterBand(1).DataType
    DataType = gdal.GetDataTypeName(DataType)
    return xsize, ysize, GeoT, Projection, DataType

# Function to write a new file.
def CreateGeoTiff(Name, Array, driver, xsize, ysize, GeoT, Projection, DataType):
    print("in creategeotiff")
    #if DataType == 'Float32':
    DataType = gdal.GDT_Float32
    NewFileName = Name
    if(not(os.path.isfile(NewFileName))):
        # Set up the dataset
        DataSet = driver.Create(NewFileName, xsize, ysize, 1, DataType) # the '1' is for band 1.
        DataSet.SetGeoTransform(GeoT)
        DataSet.SetProjection(Projection.ExportToWkt())
        # Write the array
        DataSet.GetRasterBand(1).WriteArray(Array)
        DataSet.FlushCache()
        print("new dataset created")
        return NewFileName
    else:
        print("file" + NewFileName + " already exists")

def computeNBR(nir,swir):
    print("in computeNBR")
    nbr = (nir - swir) / (nir + swir)
    return nbr
    
def readPath(image):
    print("in readPath")
    datum = image[11:27]
    name = image[38:45]
    nameDatum = name + datum
    return nameDatum
       
def readBand(filepath,image,nameDatum,band):
    print("in readBand")
    band = os.path.join(filepath,image, 'IMG_DATA', nameDatum + band + '.tif')
    if(not(os.path.isfile(band))):
        open_band = gdal.Open(band)
        img = open_band.ReadAsArray()
        img_float = img.astype(float)
        return img_float
    else:
        print("file"+ band + " is already existing")

def callNBR(nir,swir,filepath,image,nameDatum,band):
    print("in callNBR")
    band = os.path.join(filepath,image, 'IMG_DATA', nameDatum + band + '.tif')
    open_band = gdal.Open(band)
    result = computeNBR(nir,swir)
    xsize,ysize,GeoT,Projection,DataType = GetGeoInfo(band)
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    outPath = os.path.join(filepath,image, 'IMG_DATA', nameDatum + 'NBR.tif')
    if(not(os.path.isfile(outPath))):
        newFile = CreateGeoTiff(outPath,result,driver,xsize,ysize,GeoT,Projection,DataType)
        print("NBR computed")
        return result
    else:
        print("NBR with path" + outPath + " already exists")

def plot(filepath, image):
    print("in plot")
    finalPath = os.path.join(filepath,image)
    open_band = gdal.Open(finalPath)
    result1 = open_band.ReadAsArray()
    result = result1.astype(float)
    fig = plt.figure(figsize=(10, 10))
    fig.set_facecolor('white')
    plt.colorbar(plt.imshow(result, cmap=plt.cm.summer))
    plt.title('NBR')
    plt.show()

def datumCharsNBR(x):
    return(x[7:15])

def datumCharsArr(x):
    return(x[11:19])

def nbrOldNew(nbrDict,filepath):
    print("in nbrOldNew")
    for key in nbrDict:
        if(key != len(nbrDict)):
            oldNBRPath = os.path.join(filepath,nbrDict[key][1],'IMG_DATA',nbrDict[key][0])
            newNBRPath = os.path.join(filepath,nbrDict[key+1][1],'IMG_DATA',nbrDict[key+1][0])
            oldNBR = gdal.Open(oldNBRPath)
            newNBR = gdal.Open(newNBRPath)
            img_old = oldNBR.ReadAsArray()
            img_new = newNBR.ReadAsArray()
            img_oldFloat = img_old.astype(float)
            img_newFloat = img_new.astype(float)
            result = img_oldFloat - img_newFloat
            nameDatum = readPath(nbrDict[key][1])
            nameDatum2 = readPath(nbrDict[key+1][1])
            xsize,ysize,GeoT,Projection,DataType = GetGeoInfo(oldNBRPath)
            out_format = "GTiff"
            driver = gdal.GetDriverByName(out_format)
            filepath2 = filepath[:12]
            outPath = os.path.join(filepath2,'results',nameDatum + nameDatum2 + 'result_NBR.tif')
            newFile = CreateGeoTiff(outPath,result,driver,xsize,ysize,GeoT,Projection,DataType)
        else:
            print("All NBRs computed")
    

cwd = os.getcwd()
filepath = os.path.join(cwd,'test')
filepath2 = os.path.join(cwd,'results')
arr = os.listdir(filepath)
arr2 = os.listdir(filepath2)
nbrArray = []

for image in arr:
    path = readPath(image)
    resample(filepath,image,path)
    nir = readBand(filepath,image,path,"B08")
    swir = readBand(filepath,image,path,"resampleB12")
    if(nir and swir is not None):
        call_nbr = callNBR(nir,swir,filepath,image,path,"B08")
        join = path+"NBR.tif"
        nbrArray.append(join)

sortedNBR = sorted(nbrArray, key = datumCharsNBR)
sortedArr = sorted(arr, key = datumCharsArr)

nbrDict = {}
counter = 1
for nbr, path in zip(sortedNBR,sortedArr):
    nbrDict[counter] = (nbr,path)
    counter += 1

nbrOldNew(nbrDict,filepath)
##plot(filepath2,arr2[0])








