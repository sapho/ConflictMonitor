# ConflictMonitor
Monitoring Conflict Areas with Satellite Image Time Series

## Aim:
This container aims to automate the pre-processing of Sentinel-2 data from L1C to L2A.
 It uses sen2cor, see http://step.esa.int/main/third-party-plugins-2/sen2cor/.
 
## Usage:
To use this container run the script apply_sen2cor.bat.

 ```bash
cd pre_processing
docker build --tag monconfsat_pre .
cd ..
docker run --rm -v ${PWD}/data:/workspace/data -e imgfolder=/workspace/data monconfsat_pre
```
 Debug within container:
 ```bash
docker run --rm -it -v ${PWD}/data:/workspace/data -e imgfolder=/workspace/data --entrypoint=/bin/bash monconfsat_pre
```
 `LA2_Process` documentation:
 ```bash
docker run --rm -it --entrypoint=/bin/bash monconfsat_pre L2A_Process --help
```
 ## Required structure: (deprecated)
This container requires a specific folder structure to work:
 ```bash
.
|---data
|   |---S2B_MSIL1C...
|       |---S2B_MSIL1C[...].SAFE
|
|---pre_processing
|   |---apply_sen2cor.bat
|   |---apply_sen2cor.py
|   |---Dockerfile
|
|---.gitignore
|
|---portainer.bat
|
|---README.md
```          
 
Sentinel-2 data can be aquired at [ESA-Hub](https://scihub.copernicus.eu/dhus/#/home). <br>
Direct download-link to example data: [example](https://scihub.copernicus.eu/dhus/odata/v1/Products('eff34131-ccbf-4c5e-a3d6-7caa320445d8')/$value)       
