# Data Lake

```
A data lake is usually a single store of all enterprise data including raw copies of source system data and transformed data used for tasks such as reporting, visualization, advanced analytics and machine learning.

Data Lake is an accelerated system based on optimised Amazon Web Services which performs Big Data or ETL jobs.
```

# Prerequisites

If you wish to install Django using the Ubuntu repositories, the process is very straightforward.

First, update your local package index with apt:

```
sudo apt update
```

Next, check which version of Python you have installed. 18.04 ships with Python 3.6 by default, which you can verify by typing if you get an error then add your python3 path to system path variable:

```
python3 - V
```

Next, install Django:

```
sudo apt install python3-django
```

You can test that the installation was successful by typing:

```
django-admin --version
```

Next, install Python Virtual Env:

```
sudo apt install python3-venv
```
Finally
```
1) Rename ".env.sample" file to ".env"
2) Then updated values for "aws_iam_secret_key" & "aws_iam_access_id" at the end of ".env" file
```

# Usage

Use the make tool to enable and setup DLA environment.

```
make cf //one time only
```

```
make all
```
Then
```
Make a post request on localhost:8080/ 
With a payload inside form-data with a key ="file" of type="file" &
then browse and select file from these three file formats (csv,json,xml)
```
