# ConflictMonitor
Monitoring Conflict Areas with Satellite Image Time Series.

## Aim:
Investigate the damage caused by the forest fires in Protugal.
 
## Usage:
Create data directory on root

 ```bash
-/data/
    -change/
    -input/
    -nbr/
    -output/
    -raw/
    -results/
```
On Linux:
 ```bash
sudo bash startdocker.sh
```
or
 ```bash
docker build -t app/conflict_monitoring .
docker run -ti -v /var/run/docker.sock:/var/run/docker.sock -v /data:/data -p 8080:8080 app/conflict_monitoring
```

On Windows:
 ```bash
docker build -t app/conflict_monitoring .
docker run -ti -v //var/run/docker.sock://var/run/docker.sock -v /data:/data -p 8080:8080 app/conflict_monitoring
```
