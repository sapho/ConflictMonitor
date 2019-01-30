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

## Define an AOI (either matrix, sf or sp object)
data("aoi_data") # example aoi

aoi <- aoi_data[[3]] # AOI as matrix object, or better:
aoi <- aoi_data[[2]] # AOI as sp object, or:
aoi <- aoi_data[[1]] # AOI as sf object
#instead, you could define an AOI yourself, e.g. as simple matrix

## set AOI for this session
set_aoi(aoi)
view_aoi() #view AOI in viewer, which will look like this:

#instead of using an existing AOI, you can simply draw one:
set_aoi() #call set_aoi() without argument, which opens a mapedit editor:

## After defining a session AOI, define time range and platform
time_range <-  c("2018-07-01", "2018-09-30")
platform <- "Sentinel-2" #or "Sentinel-1" or "Sentinel-3"

## set login credentials and archive directory
login_CopHub(username = "sapho") #asks for password or define 'password'
set_archive("/data/raw")

## Use getSentinel_query to search for data (using the session AOI)
records <- getSentinel_query(time_range = time_range, platform = platform)

## Filter the records
colnames(records) #see all available filter attributes
unique(records$processinglevel) #use one of the, e.g. to see available processing levels

records_filtered <- records[which(records$processinglevel == "Level-1C"),] #filter by Level
records_filtered <- records_filtered[as.numeric(records_filtered$cloudcoverpercentage) <= 30, ] #filter by clouds

## View records table
View(records)
View(records_filtered)
#browser records or your filtered records

## Preview a single record on a mapview map with session AOI
getSentinel_preview(record = records_filtered[9,])

## Preview a single record on a mapview map without session AOI
getSentinel_preview(record = records_filtered[9,], show_aoi = FALSE)

## Preview a single record as RGB plot
getSentinel_preview(record = records_filtered[9,], on_map = FALSE)

## Download some datasets to your archive directory
datasets <- getSentinel_data(records = records_filtered[c(4,7,9), ])

## Finally, define an output format and make them ready-to-use
datasets_prep <- prepSentinel(datasets, format = "tiff")
# or use VRT to not store duplicates of different formats
datasets_prep <- prepSentinel(datasets, format = "vrt")

## View the files
datasets_prep[[1]][[1]][1] #first dataset, first tile, 10 m resolution
datasets_prep[[1]][[1]][2] #first dataset, first tile, 20 m resolution
datasets_prep[[1]][[1]][3] #first dataset, first tile, 60 m resolution

## Load them directly into R
r <- stack(datasets_prep[[1]][[1]][1])
