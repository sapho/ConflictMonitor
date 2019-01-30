## Install packages
install.packages("devtools")
devtools::install_github("16EAGLE/getSpatialData")
install.packages("raster")
install.packages("sf")
install.packages("sp")

## Load packages
library(getSpatialData)
library(raster)
library(sf)
library(sp)

## Define a polygon enclosing the Rakhine State of Myanmar as a SpatialPolygons feature
x_coord <- c(92.37145,  91.93209,  92.40440, 93.22819, 94.42545, 94.94169, 94.96366, 94.57922, 93.95314, 92.37145)
y_coord <- c(21.63687, 21.22769, 20.13790, 19.06123, 17.23382, 17.28629, 18.50981, 19.61082, 20.86872, 21.63687)
xym <- cbind(x_coord, y_coord)

p = Polygon(xym)
ps = Polygons(list(p),1)
aoi = SpatialPolygons(list(ps))

proj4string(aoi) = CRS("+proj=longlat +datum=WGS84 +no_defs +ellps=WGS84 +towgs84=0,0,0")

# set the SpatialPolygons feature as AOI
set_aoi(aoi)

## After defining a session AOI, define time range and platform
time_range <-  c("2018-07-01", toString(Sys.Date()))
platform <- "Sentinel-2" #or "Sentinel-1" or "Sentinel-3"

## set login credentials and archive directory
login_CopHub(username = "conflictmonitor", password = "conflictmonitor2019")

## Use getSentinel_query to search for data (using the session AOI)
records <- getSentinel_query(time_range = time_range, platform = platform)

## Filter the records
colnames(records) #see all available filter attributes
unique(records$processinglevel) #use one of the, e.g. to see available processing levels

records_filtered <- records[which(records$processinglevel == "Level-1C"),] #filter by Level
records_filtered <- records_filtered[as.numeric(records_filtered$cloudcoverpercentage) <= 30, ] #filter by clouds

## Download some datasets to your archive directory
dir.create("/data/")
dir.create("/data/raw/")
dir.create("/data/raw/zipped")
set_archive("/data/raw/zipped")
datasets <- getSentinel_data(records = records_filtered[c(1,5), ])

## Extract datasets to your unzip directory
dir.create("/data/raw/unzipped")
for (i in 0:(length(datasets)-1)) {
  i <- i+1
  unzip (datasets[i], exdir = "/data/raw/unzipped")
}
remove(i)
