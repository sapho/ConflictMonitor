# Image Manipulation for Change Detection

### Required Folderstructure
```bash
├── ImageManipulation
│   ├── tifs (exactly 2 .tifs inside)
│   │   ├── *tif1.tif
│   │   ├── *tif2.tif
│   ├── result (**Generated on script.py if not already existing)
│   │   ├── *result.tif (**Generated on script.py execution)
│   ├── script.py
```

### Usage
```bash
$ cd ImageManipulation
$ python3 script.py
```

### Treshold
If you want to change the treshold limit, look for the following line in the script.py and change the value accordingly.

```python
thresholdLimit = 500
```


### Filtering
Filtering of salt & pepper noise is done by using a median-filter.
If you want to change the median filter size, look for the following line in the script.py and change the value accordingly.

```python
filterLimit = 4
```