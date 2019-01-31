import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from osgeo import gdal
import fnmatch
from gdalconst import *
from osgeo import osr
import shutil
from os import system

def moveImage(filepath,image):
    imagePath = os.path.join(filepath,image,"GRANULE")
    dstPath = os.path.join(filepath,image,"IMG_DATA")
    folder = os.listdir(imagePath)
    print(not(os.path.isdir(dstPath)))
    if(not(os.path.isdir(dstPath))):
        for directory in folder:
            imgFolder = os.path.join(filepath,image,"GRANULE",directory,"IMG_DATA")
            shutil.copytree(imgFolder,dstPath)
    else:
        print("img folder already moved")
    

def jp2ToTiff(filepath,image):
    path = os.path.join(filepath,image,"IMG_DATA")
    resolutions = os.listdir(path)
    for resolution in resolutions:
        bandPath = os.path.join(filepath,image,"IMG_DATA",resolution)
        bands = os.listdir(bandPath)
        for band in bands:
            images = os.path.join(filepath,image,"IMG_DATA",resolution,band)
            in_image = gdal.Open(images)
            driver = gdal.GetDriverByName("GTiff")
            out_image = driver.CreateCopy(images[0:len(images)-4] + ".tif",in_image,0)
    
   

def resample(filepath,image,resolution,name_datum,band,outRes,x,y,resAlg,outputT):
    print("in resample")
    resampleBandPath = os.path.join(filepath,image,"IMG_DATA",resolution,name_datum + band + ".tif")
    resampleBand = gdal.Open(resampleBandPath)
    getBand = resampleBand.GetRasterBand(1)
    outFile = os.path.join(filepath, image,"IMG_DATA",outRes,name_datum + "resample" + band + ".tif")
    if(not(os.path.isfile(outFile))):
        result = gdal.Translate(outFile,resampleBandPath,format="GTiff",width=x,height=y,resampleAlg=resAlg,outputType=outputT)
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

def callNBR(nir,swir,filepath,image,resolution,nameDatum,band):
    print("in callNBR")
    inPath = os.path.join(filepath,image,'IMG_DATA',resolution, nameDatum + band + '.tif')
    open_band = gdal.Open(inPath)
    result = computeNBR(nir,swir)
    xsize,ysize,GeoT,Projection,DataType = GetGeoInfo(inPath)
    format_out = "GTiff"
    driver = gdal.GetDriverByName(format_out)
    outPath = os.path.join(filepath,'nbr',image, 'IMG_DATA', resolution, nameDatum + 'NBR.tif')
    print("OutPath: " + outPath)
    print(not(os.path.isfile(outPath)))
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

def nbrOldNew(nbrDict,filepath,filepath2,resolution):
    print("in nbrOldNew")
    for key in nbrDict:
        if(key != len(nbrDict)):
            oldNBRPath = os.path.join(filepath,nbrDict[key][1],'IMG_DATA',resolution,nbrDict[key][0])
            newNBRPath = os.path.join(filepath,nbrDict[key+1][1],'IMG_DATA',resolution,nbrDict[key+1][0])
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
            outPath = os.path.join(filepath2,nameDatum + nameDatum2 + 'result_NBR.tif')
            newFile = CreateGeoTiff(outPath,result,driver,xsize,ysize,GeoT,Projection,DataType)
        else:
            print("All NBRs computed")

cwd = os.getcwd()
root = os.path.dirname(cwd)
filepath = os.path.join(root,'data','input')
filepath2 = os.path.join(root,'data','nbr')
arr = os.listdir(filepath)
arr.remove("results")
arr2 = os.listdir(filepath2)
nbrArray = []


for image in arr:
    moveImage(filepath,image)
    jp2ToTiff(filepath,image)  
    path = readPath(image)
    resample(filepath,image,"R20m",path,"B12_20m","R10m",10980,10980,"nearest",gdal.GDT_Float32)
    nir = readBand(filepath,image,"R10m",path,"B08_10m")
    swir = readBand(filepath,image,"R10m",path,"resampleB12_20m")
    if(np.all(nir) is not None and np.all(swir) is not None):
        call_nbr = callNBR(nir,swir,filepath,image,"R10m",path,"B08_10m")
        join = path+"NBR.tif"
        nbrArray.append(join)

sortedNBR = sorted(nbrArray, key = datumCharsNBR)
sortedArr = sorted(arr, key = datumCharsArr)

nbrDict = {}
counter = 1
for nbr, path in zip(sortedNBR,sortedArr):
    nbrDict[counter] = (nbr,path)
    counter += 1

nbrOldNew(nbrDict,filepath,filepath2,"R10m")
#for image2 in arr2:
#    plot(filepath2,image2)
#plot(filepath2,arr2[2])








