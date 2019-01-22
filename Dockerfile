FROM ubuntu

ENV TERM=xterm\
    TZ=Europe/Berlin\
    DEBIAN_FRONTEND=noninteractive


RUN apt-get update && apt-get install -y python python3 python-pip python3-pip python-dev python3-dev curl software-properties-common

RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable && apt-get update

RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -yq nodejs build-essential
RUN npm install -g npm

RUN apt-get update && apt-get remove -y python && apt-get install -y nodejs r-base libudunits2-dev libgit2-dev libssh2-1-dev libgdal-dev libgdal20 libproj-dev binutils gdal-bin

RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

RUN pip3 install numpy
RUN pip3 install wheel
RUN pip3 install osr
RUN pip3 install GDAL==2.3.
#RUN pip3 install time
#RUN pip3 install copy
RUN pip3 install Pillow
RUN pip3 install sklearn
RUN pip3 install scipy
RUN pip3 install opencv-python

RUN mkdir /imageAcquisition
COPY imageAcquisition/getSpatialData.R /imageAcquisition
#RUN Rscript /imageAcquisition/getSpatialData.R

WORKDIR /usr/src/monitoringApp2

RUN mkdir /server

RUN mkdir /pre_pocessing
ADD pre_processing/* ./pre_processing/

RUN mkdir /data
ADD data/* ./data/

COPY server/package*.json /server
WORKDIR /server
RUN npm install

WORKDIR ../

COPY . .

WORKDIR /server

EXPOSE 8080

CMD [ "npm", "start"]
