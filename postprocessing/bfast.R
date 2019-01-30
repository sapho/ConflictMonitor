install.packages("devtools")
library(devtools)
install_github('loicdtx/bfastSpatial')
install_github("appelmar/strucchange")
install_github("appelmar/bfast")
install_github("ozjimbob/ecbtools",force=T)
install.packages('Rcpp')
install.packages("raster")
install.packages("reticulate")
# load the package
library(bfastSpatial)
library(bfast)
library(strucchange)
library(raster)
library(reticulate)

set_fast_options() 

dates = function(files){
  dateList = list()
  for (file in files){
    result = substr(file,start = 31, stop = 38)
    dateList[[file]] <- result
  }
  return (dateList)
}

decDateToJulian = function(dates){
  result = list()
    x = dates[!is.na(dates)]
    x = as.numeric(as.character(x))
    yrs = as.numeric(substr(as.character(x),1,4))
    x = x - yrs
    x = x * 365
    x = paste(yrs,x,sep="")
    x = as.Date(x,format="%Y%j")
    result = x

  return (result)
} 

compare = function(result,asDate){
  for(x in asDate){
      if(result > x){
        print('not Found')
      } else {
        return (as.Date(x))
      }
  }
}


setwd("../data/nbr/subsets")
#setwd("F:/1MCASITS/subsets2")
wd = getwd()

path = list.files(wd, pattern = '.tif')
#pathTest = list.files("D:/1MCASITS/subsets", pattern = '.tif')

#Example data
#data(tura)
#system.time(bfm <- bfmSpatial(tura, start=c(2009, 13)))

# Stack the layers
s = stack(path)
#extract dates
fileDates = dates(path)
#create data frame with transponsed dates
dateFrame = as.data.frame(fileDates)
transpose = data.frame(t(dateFrame))
asDate = as.Date(paste(transpose$t.dateFrame.),'%Y%m%d')
asDate
#Set Z component for algorithm
s = setZ(x=s,z=asDate)
#Apply fmfSpatial
print("start bfm calculation")
bfmTime = system.time(bfm <- bfmSpatial(s,asDate,pptype = 'irregular',start = c(2017,1),history = 'all'))
bfmTime
#plot(bfm)
breakpoints = raster(bfm,1)
breakpoints = breakpoints[!is.na(breakpoints)]
### Input for Image manipulation (Viktor)
counts = table(breakpoints)
counts_df = as.data.frame(counts)
sort = counts_df[order(counts_df$Freq,decreasing = T),]
frequent = sort[1:3,]
result = decDateToJulian(frequent$breakpoints)
nextDate1 = compare(result[1],asDate)
nextDate2 = compare(result[2],asDate)
nextDate3 = compare(result[3],asDate)
datenew1 = gsub("-","",nextDate1)
datenew2 = gsub("-","",nextDate2)
datenew3 = gsub("-","",nextDate3)
grep1 = grep(datenew1,path,value=T)
grep2 = grep(datenew2,path,value=T)
grep3 = grep(datenew3,path,value=T)
print("starting with k-means")
### Apply k-means
breaks = raster(bfm,1)
magnitude = raster(bfm,2) 
magnitude[is.na(breaks)] <- NA
clusters = kmeans(na.omit(magnitude@data@values),10,nstart = 20)
valueTable = getValues(brick(magnitude))
head(valueTable)
rNA = setValues(raster(magnitude),NA)
rNA[is.na(magnitude)] = 1
rNA = getValues(rNA)
rNA[is.na(rNA)] = 0
valueTable = as.data.frame(valueTable)
valueTable$magnitude[rNA=0] = clusters$cluster
valueTable$magnitude[rNA=1] = NA
classes = raster(magnitude)
classes = setValues(classes,valueTable$magnitude)
png(filename="../bfastPlots/magnitude.png")
plot(classes, col = rainbow(10))
dev.off()

clusters2 = kmeans(na.omit(breaks@data@values),10,nstart=20)
valueTable2 = getValues(brick(breaks))
head(valueTable2)
rNA2 = setValues(raster(breaks),NA)
rNA2[is.na(breaks)] = 1
rNA2 = getValues(rNA2)
rNA2[is.na(rNA2)] = 0
valueTable2 = as.data.frame(valueTable2)
valueTable2$breakpoint[rNA2=0] = clusters2$cluster
valueTable2$breakpoint[rNA2=1] = NA
classes2 = raster(breaks)
classes2 = setValues(classes,valueTable2$breakpoint)
png(filename="../bfastPlots/breakpoints.png")
plot(classes2, col = rainbow(10))
dev.off()

#Call changeDetect
source_python('/conflicMonitoring/postprocessing/tiffChangeDetection.py')
tiffChangeDetection(grep1[1],grep1[2],"bfast_ChangeDetection1")
tiffChangeDetection(grep2[1],grep2[2],"bfast_ChangeDetection2")
tiffChangeDetection(grep3[1],grep3[2],"bfast_ChangeDetection3")