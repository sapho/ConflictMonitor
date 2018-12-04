docker build  -t apply . 
docker run --rm --name=apply_container -e imgfolder=/workspace apply
pause
