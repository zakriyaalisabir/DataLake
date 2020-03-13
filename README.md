# Data Lake
```
A data lake is usually a single store of all enterprise data including raw copies of source system data and transformed data used for tasks such as reporting, visualization, advanced analytics and machine learning.

Data Lake is an accelerated system based on optimised Amazon Web Services which performs ETL jobs. 
```


## Prerequisites
If you wish to install Django using the Ubuntu repositories, the process is very straightforward.

First, update your local package index with apt:
```
sudo apt update
```
Next, check which version of Python you have installed. 18.04 ships with Python 3.6 by default, which you can verify by typing:
```
python3 -V
```

Next, install Django:
```
sudo apt install python3-django
```
You can test that the installation was successful by typing:
```
django-admin --version
```


## Usage

Use the make tool to enable and setup DLA environment.
```bash
make all
```