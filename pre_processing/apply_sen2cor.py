# This script combines the steps of applying sen2cor
# for atmospheric correction and building composites
# based on the scripts provided by Christian Knoth

from sys import argv
from os import system
import osgeo.gdal as gdal
import os


def run_correction_10(imgfolder):
    # list level 1C files in folder
    L1Cfiles = [s for s in os.listdir(imgfolder) if "L1C" in s]
    print(str(len(L1Cfiles)) +
          ' level 1C file(s) found. Performing atmospheric correction.')

    # run sen2cor on level 1C files
    for file in L1Cfiles:
        command = 'L2A_Process ' + \
            os.path.join(imgfolder, file) + ' --resolution=10'
        system(command)
        #print('Atmospheric correction finished for ' + file)

    print('Done.')


def run_correction_20(imgfolder):
    # list level 1C files in folder
    L1Cfiles = [s for s in os.listdir(imgfolder) if "L1C" in s]
    print(str(len(L1Cfiles)) +
          ' level 1C file(s) found. Performing atmospheric correction.')

    # run sen2cor on level 1C files
    for file in L1Cfiles:
        command = 'L2A_Process ' + \
            os.path.join(imgfolder, file) + ' --resolution=20'
        system(command)
        #print('Atmospheric correction finished for ' + file)

    print('Done.')

    
def run_correction_60(imgfolder):
    # list level 1C files in folder
    L1Cfiles = [s for s in os.listdir(imgfolder) if "L1C" in s]
    print(str(len(L1Cfiles)) +
          ' level 1C file(s) found. Performing atmospheric correction.')

    # run sen2cor on level 1C files
    for file in L1Cfiles:
        command = 'L2A_Process ' + \
            os.path.join(imgfolder, file) + ' --resolution=60'
        system(command)
        #print('Atmospheric correction finished for ' + file)

    print('Done.')


def create_composites(imgfolder, Level='2A'):

    # create folder for composites
    try:
        if not os.path.exists(os.path.join(imgfolder, 'CIR_composites')):
            os.makedirs(os.path.join(imgfolder, 'CIR_composites'))
    except OSError:
        print('Error: Creating directory',
              os.path.join(imgfolder, 'CIR_composites'))

    # list unzipped folders
    if Level == '2A':
        subfolders = [s for s in os.listdir(imgfolder) if "L2A" in s]
        print("Creating 4-band CIR composites of level 2A images...")
    else:
        subfolders = [s for s in os.listdir(imgfolder) if "L1C" in s]
        print("Creating 4-band CIR composites of level 1C images...")

    # in each folder find CIR bands and create composites
    for folder in subfolders:
        # navigate through GRANULE folder to band files
        granule_folder = os.listdir(
            os.path.join(imgfolder, folder, 'GRANULE'))[0]
        if Level == '2A':
            bands_path = os.path.join(
                imgfolder, folder, 'GRANULE', granule_folder, 'IMG_DATA', 'R10M')
        else:
            bands_path = os.path.join(
                imgfolder, folder, 'GRANULE', granule_folder, 'IMG_DATA')
        # create list of paths to the CIR bands, search by name to be independent from number of files in folder
        CIR_bandpaths = [os.path.join(bands_path, [s for s in os.listdir(bands_path) if "B02" in s][0]),
                         os.path.join(bands_path, [s for s in os.listdir(
                             bands_path) if "B03" in s][0]),
                         os.path.join(bands_path, [s for s in os.listdir(
                             bands_path) if "B04" in s][0]),
                         os.path.join(bands_path, [s for s in os.listdir(bands_path) if "B08" in s][0])]

        # create virtual layer
        outvrt = '/vsimem/composite.vrt'  # /in-memory virtual directory

        # create subfolder for current image composite
        composite_path = os.path.join(imgfolder, 'CIR_composites', folder)
        try:
            if not os.path.exists(composite_path):
                os.makedirs(composite_path)
        except OSError:
            print('Error: Creating directory. ' + composite_path)

        # create composite in composite folder
        composite_name = granule_folder.split("_")[3] + '_composite.tif'
        outtif = os.path.join(composite_path, composite_name)
        outds = gdal.BuildVRT(outvrt, CIR_bandpaths, separate=True)
        outds = gdal.Translate(outtif, outds)
        print("Composite created for " + granule_folder)

    print("Finished. All composites can be found in folder " +
          imgfolder + '\CIR_composites.')


if __name__ == "__main__":
    imgfolder = os.environ['imgfolder']
    level = '2A'
    run_correction_10(imgfolder)
    # run_correction_20(imgfolder)
    # run_correction_60(imgfolder)
    create_composites(imgfolder, level)
