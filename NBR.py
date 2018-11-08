import rasterio
import rasterio.plot
import pyproj
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os
from osgeo import gdal

def reproject(nir, filepath, image, img_data):
    with rasterio.open(nir) as src:
        src_transform = src.transform
        dst_transform = src_transform*A.translation(
        -src.width/2.0, -src.height/2.0)*A.scale(2.0)
        data = src.read()
        kwargs = src.meta
        kwargs['transform'] = dst_transform
        newPath = os.path.join(filepath,image, img_data,'zoomed_out_nir.tif')
        with rasterio.open(newPath, 'w', **kwargs) as dst:
            for i, band in enumerate(data, 1):
                dest = np.zeros_like(band)
                reproject(
                    band,
                    dest,
                    src_transform=src_transform,
                    src_crs=src.crs,
                    dst_transform=dst_transform,
                    dst_crs=src.crs,
                    resampling=Resampling.nearest)
                dst.write(dest, indexes=i)

def nbr(nir,swir):
    nbr = (nir - swir) / (nir + swir)
    return nbr

def nbrOldNew():
    oldNBRPath = os.path.join('F://','1MCASITS','test','S2A_MSIL1C_20180104T042151_N0206_R090_T46QDJ_20180104T074740.SAFE','IMG_DATA','T46QDJ_20180104T042151_NBR.PNG')
    newNBRPath = os.path.join('F://','1MCASITS','test','S2B_MSIL1C_20180109T042139_N0206_R090_T46QDJ_20180109T144840.SAFE','IMG_DATA','T46QDJ_20180109T042139_NBR.PNG')
    oldNBR = gdal.Open(oldNBRPath)
    newNBR = gdal.Open(newNBRPath)
    img_old = oldNBR.ReadAsArray()
    img_new = newNBR.ReadAsArray()
    result = img_old - img_new
    format2 = "PNG"
    driver = gdal.GetDriverByName(format2)
    outPath = os.path.join('F://','1MCASITS','results','result_NBR.PNG')
    outDataRaster = driver.CreateCopy(outPath,oldNBR,0)
    outDataRaster.GetRasterBand(1).WriteArray(result)
    #print result[[]]
    fig = plt.figure(figsize=(10, 10))
    fig.set_facecolor('white')
    #plt.imshow(result, cmap=plt.cm.summer) # Typically the color map for NBR maps are the Red to Yellow to Green
    plt.colorbar(plt.imshow(result, cmap=plt.cm.summer))
    plt.title('NBR')
    plt.show()
    

print('Load images')

filepath = os.path.join('F://','1MCASITS','test')
arr = os.listdir(filepath)
print(arr)

nbrOldNew()
##for image in arr:
##    image = 'S2A_MSIL1C_20180104T042151_N0206_R090_T46QDJ_20180104T074740.SAFE'
##    datum = image[11:27]
##    name = image[38:45]
##    nameDatum = name + datum
##    nir = os.path.join(filepath, image, 'IMG_DATA', nameDatum + 'B08.PNG')
##    #swir = os.path.join(filepath, image, 'IMG_DATA', nameDatum + 'B12.PNG')
##    swir = os.path.join(filepath, image, 'IMG_DATA', nameDatum + 'B13.PNG')
##    nir2 = gdal.Open(nir)
##    swir2 = gdal.Open(swir)
##    img_nir = nir2.ReadAsArray()
##    img_swir = swir2.ReadAsArray()
##    img_nir.astype(float)
##    img_swir.astype(float)
##    #reproject(nir,filepath,image,'IMG_DATA')
##    #nir2 = os.path.join(filepath, image, 'IMG_DATA', nameDatum + 'zoomed_out_nir.PNG')
##    result = nbr(img_nir,img_swir)
##    format2 = "PNG"
##    driver = gdal.GetDriverByName(format2)
##    outPath = os.path.join(filepath, image, 'IMG_DATA', nameDatum + 'NBR.PNG')
##    outDataRaster = driver.CreateCopy(outPath,nir2,0)
##    outDataRaster.GetRasterBand(1).WriteArray(result)
##    fig = plt.figure(figsize=(10, 10))
##    fig.set_facecolor('white')
##    plt.imshow(result, cmap='RdYlGn') # Typically the color map for NBR maps are the Red to Yellow to Green
##    plt.title('NBR')
##    plt.show()
