# This script simply executes the sen2cor processor on all unzipped L1C Sentinel-2 files in a folder.
# Takes one input argument, the directory where the unzipped L1C files are
# sen2cor needs to be installed (standalone installer) and the directory containing
# "L2A_Process.bat" needs to be added to path system environment variable


from sys import argv
from os import system

import os


def run_correction(imgfolder):
    # list level 1C files in folder
    L1Cfiles = [s for s in os.listdir(imgfolder) if "L1C" in s]
    print(str(len(L1Cfiles)) + ' level 1C file(s) found. Performing atmospheric correction.')

    # run sen2cor on level 1C files
    for file in L1Cfiles:
        command = 'L2A_Process ' + os.path.join(imgfolder, file) + ' --resolution=10'
        system(command)
        #print('Atmospheric correction finished for ' + file)

    print('Done.')


if __name__ == "__main__":
    imgfolder = os.environ['imgfolder']
    run_correction(imgfolder)
