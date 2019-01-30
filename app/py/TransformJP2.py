import os
from pgmagick import Image

# Input path for jp2 files
inputPath = ".\input"
# Output path for png files
outputPath = '.\output'

def getfiles():
    for root, dirs, files in os.walk(inputPath):  
        for currFile in files:
            filename = currFile.split(".")[0]
            extension = currFile.split(".")[1]
            if (extension == 'jp2' and 'TCI' in filename):
                path = os.path.join(inputPath, currFile)
                img = Image(path)
                img.write(os.path.join(outputPath, filename + os.extsep + 'png'))

getfiles()