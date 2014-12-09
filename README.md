![alt tag](https://github.com/MBoustani/GISCube/blob/master/giscube_app/static/img/logo.png)
=======

## Web Baised GIS Application


Beside some open source GIS libraries and some software like ArcGIS there are comparatively few open source, web-based and easy to use application that are capable of doing GIS processing and visualization. To address this, we present GISCube, an open source web-based GIS application that can store, visualize and process GIS and GeoSpatial data. GISCube is powered by [Geothon](https://github.com/MBoustani/Geothon), an open source python GIS cookbook. Geothon has a variety of Geoprocessing tools such data conversion, processing, spatial analysis and data management tools. GISCube has the capability of supporting a variety of well known GIS data formats in both vector and raster formats, and the system is being expanded to support NASA’s and scientific data formats such as netCDF and HDF files. In this talk, we demonstrate how Earth science and other projects can benefit by using GISCube and Geothon, its current goals and our future work in the area.

#Easy installation (vagrant)

1- [Install Vagrant](https://docs.vagrantup.com/v2/installation/)

2- Download [vagrant.zip](https://github.com/MBoustani/GISCube/raw/master/vagrant.zip)

3- Unzip vagrant.zip

4- `cd vagrant`

5- `vagrant init`

6- `vagrant up`

7- `vagrant ssh`

8- `git clone https://github.com/MBoustani/GISCube.git GISCube`

9- `python GISCube/manage.py runserver 0.0.0.0:5050`

10- open [test](localhost:5050) in browser and enjoy.


[Documentation](https://github.com/MBoustani/GISCube/wiki)


