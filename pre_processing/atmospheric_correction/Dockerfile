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
		python2.7 \
      python-pip \
      wget \
      file \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install numpy 
RUN pip install numpy

# Install Sen2Cor
ENV SEN2COR_VERSION='Sen2Cor-02.05.05-Linux64'
RUN mkdir /sen2cor
WORKDIR /sen2cor

RUN wget http://step.esa.int/thirdparties/sen2cor/2.5.5/$SEN2COR_VERSION.run -P . \
    && bash /sen2cor/$SEN2COR_VERSION.run \
    && rm -rf ${SEN2COR_VERSION}.run

# Set path to make Sen2Cor usable
ENV PATH="/sen2cor/$SEN2COR_VERSION/bin:$PATH"

# Use Saphir's downloaded data @/data/raw/unzipped
ENV imgfolder = /data/raw/unzipped

# Run apply_sen2cor.py when the container launches
ENTRYPOINT ["python"]
CMD ["apply_sen2cor.py"]  