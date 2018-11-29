library(devtools)
install_github('loicdtx/bfastSpatial')
install_github("appelmar/strucchange")
install_github("appelmar/bfast")
install.packages('Rcpp')
# load the package
library(bfastSpatial)
library(bfast)

set_fast_options() 

dates = function(files){
  dateList = list()
  for (file in files){
    result = substr(file,start = 8, stop = 15)
    dateList[[file]] <- result
  }
  return (dateList)
}

setwd("D:/1MCASITS/results")
wd = getwd()

path = list.files(wd, pattern = '.tif')

dirout = file.path(wd,'stack')
dir.create(dirout, showWarnings=FALSE)

# Generate a file name for the output stack
stackName = file.path(dirout, 'stackTest.tif')

# Stack the layers
s = stack(path)
fileDates = dates(path)
fileDates
dateFrame = as.data.frame(fileDates)
transpose = data.frame(t(dateFrame))
asDate = as.Date(paste(transpose$t.dateFrame.),'%Y%m%d')
bfmObject = system.time(bfm <- bfmSpatial(s, asDate ,pptype = 'irregular',start = c(2018,1)))
system.time(bfm <- bfmSpatial(tura, start=c(2009, 13)))

# Visualize both layers (They are the same for the reason stated above)
plot(s[[1]])




