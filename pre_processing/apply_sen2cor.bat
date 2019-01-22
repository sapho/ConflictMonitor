docker build -t apply . 
docker run --name=apply_container -e imgfolder=/workspace apply
docker cp apply_container:/workspace .
docker rm -f apply_container
pause
