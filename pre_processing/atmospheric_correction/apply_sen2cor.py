from sys import argv
from os import system
import os

# This script simply executes the sen2cor processor on all unzipped L1C Sentinel-2 files in a folder.
# Takes one input argument, the directory where the unzipped L1C files are
# Based on the script provided by Christian Knoth @[www.github.com/DaChro/get-sen2-py]
def run_correction(imgfolder, resolution):
    
    # list level 1C files in folder
    L1Cfiles = [s for s in os.listdir(imgfolder) if "L1C" in s]
    print(str(len(L1Cfiles)) +
          ' level 1C file(s) found. Performing atmospheric correction.')

    # run sen2cor on level 1C files
    for file in L1Cfiles:
        command = 'L2A_Process ' + \
            os.path.join(imgfolder, file) + resolution
        system(command)

    print('Done.')


if __name__ == "__main__":
    
    # set imgfolder (= folder containing L1C data) using environment variable
    # this should point to the .SAFE folder
    imgfolder = os.environ['imgfolder']

    run_correction(imgfolder, ' --resolution=10')
    # Available bands in resolution 10m: 
    # AOT, B02, B03, B04, B08, TCI, WVP

    run_correction(imgfolder, ' --resolution=20')
    # Available bands in resolution 20m: 
    # AOT, B02, B03, B04, B05, B06, B07, B8A, B11, B12, SCL, TCI, WVP

    run_correction(imgfolder, ' --resolution=60')
    # Available bands in resolution 60m: 
    # AOT, B01, B02, B03, B04, B05, B06, B07, B8A, B09, B11, B12, SCL, TCI, WVP
