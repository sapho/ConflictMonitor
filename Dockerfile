FROM node:8

WORKDIR /usr/src/monitoringApp

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
