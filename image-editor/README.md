# Install


```
pip install -r requirements.txt
pip install GDAL-3.0.1-cp37-cp37m-win32.whl
pip install rasterio-1.0.27-cp37-cp37m-win32.whl
```


## Windows
```
```

## Linux
```
```

# fix ubuntu problems
```
https://forum.openoffice.org/en/forum/viewtopic.php?f=16&t=95150
sudo dpkg -P openoffice-debian-menus
sudo apt --fix-broken install
```

#fix bug with pillow DLL on windows
```
conda uninstall pillow
conda install pillow 
```

#Build

````
pyinstaller.exe --onefile --icon=myicon.ico main.py

````