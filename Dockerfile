FROM ubuntu

ENV TERM=xterm\
    TZ=Europe/Berlin\
    DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/src/monitoringApp

# Install python and repository for gdal
RUN apt-get update && apt-get install -y python python3 python-pip python3-pip python-dev python3-dev python-setuptools python3-setuptools curl software-properties-common apt-transport-https ca-certificates
RUN add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable && apt-get update

# Install node/npm
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash
RUN apt-get install -yq nodejs build-essential
RUN npm install -g npm

RUN apt-get update && apt-get install -y r-base libudunits2-dev libgit2-dev libssh2-1-dev libgdal-dev libgdal20 libproj-dev binutils gdal-bin

#Install docker
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
RUN apt-key fingerprint 0EBFCD88
RUN add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
RUN apt-get update && apt-get install -y docker-ce

# Export paths for gdal
RUN export CPLUS_INCLUDE_PATH=/usr/include/gdal
RUN export C_INCLUDE_PATH=/usr/include/gdal

# Install python3 packages
RUN pip3 install numpy
RUN pip3 install wheel
RUN pip3 install osr
RUN pip3 install GDAL==2.3
RUN pip3 install Pillow
RUN pip3 install sklearn
RUN pip3 install scipy
RUN pip3 install opencv-python

# Install python2 packages
RUN pip install pyproj
RUN pip install numpy
RUN pip install matplotlib
RUN pip install wheel
RUN pip install osr
RUN pip install GDAL==2.3
RUN pip install requests
RUN pip install --upgrade setuptools
RUN pip install sentinelsat

COPY getSpatialData.R .

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
