## Install packages
install.packages("devtools")
devtools::install_github("16EAGLE/getSpatialData")
install.packages("sp")

## Load packages
library(getSpatialData)
library(sp)

## Define a polygon enclosing the Rakhine State of Myanmar as a SpatialPolygons feature
x_coord <- c(92.37145,  91.93209,  92.40440, 93.22819, 94.42545, 94.94169, 94.96366, 94.57922, 93.95314, 92.37145)
y_coord <- c(21.63687, 21.22769, 20.13790, 19.06123, 17.23382, 17.28629, 18.50981, 19.61082, 20.86872, 21.63687)
xym <- cbind(x_coord, y_coord)

p <- Polygon(xym)
ps <- Polygons(list(p),1)
aoi <- SpatialPolygons(list(ps))

proj4string(aoi) <- CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")

## Set the SpatialPolygons feature as AOI
set_aoi(aoi)

## Define time ranging a fortnight into the past from current date and set platform
time_range <-  c(toString(Sys.Date() - 14), toString(Sys.Date()))
platform <- "Sentinel-2"

## Set login credentials
login_CopHub(username = "conflictmonitor", password = "conflictmonitor2019")

## Use getSentinel_query to search for data within AOI
records <- getSentinel_query(time_range = time_range, platform = platform)

## Filter the records
records_filtered <- records[which(records$processinglevel == "Level-1C"),]
records_filtered <- records_filtered[as.numeric(records_filtered$cloudcoverpercentage) <= 30, ]

## Download queried datasets to archive directory
dir.create("/data/raw/zipped", recursive = TRUE)
set_archive("/data/raw/zipped")

datasets <- getSentinel_data(records = records_filtered)

## Extract downloaded datasets to unzip directory
dir.create("/data/raw/unzipped")
for (i in 0:(length(datasets)-1)) {
  i <- i+1
  unzip (datasets[i], exdir = "/data/raw/unzipped")
}
remove(i)

## Copy all JPEG 2000 (jp2) files of each dataset from dispersed subfolders into one dedicated jp2 directory [optional]
# ext <- ".jp2"
# unzipped_files <- list.files(path = "/data/raw/unzipped", full.names = TRUE, recursive = TRUE, include.dirs = TRUE)
# dir.create("/data/raw/jp2")
# sapply(unzipped_files[grep(ext, unzipped_files)], FUN=function(x) file.copy(from = x, to = "/data/raw/jp2"))
