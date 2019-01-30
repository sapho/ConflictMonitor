# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

FROM ubuntu:18.04
MAINTAINER Sebastian Holtkamp <Sebastian.Holtkamp@wwu.de>

# Install dependencies 
RUN apt-get update \
   && apt-get install -qqy --no-install-recommends \
      software-properties-common \
      wget \
      file \
   && add-apt-repository -y ppa:ubuntugis/ubuntugis-unstable \
   && apt-get update \
   && apt-get install -qqy --no-install-recommends \
       python2.7 \
       python-pip \
       gdal-bin \
       python-gdal \
       libopenjp2-7-dev \
       libgdal-dev

# Install numpy 
RUN pip install numpy

# Make workspace and copy all files of current directory into it 
WORKDIR /workspace
COPY . /workspace

# Run composites.py when the container launches
ENTRYPOINT ["python"]
CMD ["composites.py"] 
