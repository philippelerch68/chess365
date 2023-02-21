## Table of Contents
1. [General Info](#general-info)
2. [Expectation](#Expectation)
3. [Modules](#Modules)
4. [Minimum Requirements](#Minimum-Requirements)
5. [Run the process](#Run-the-process)

## General Info
***
The aim of this project is a data engineering pipeline in the form of an ELT process, which loads chess data of 200 Players and their Game history. The data is loaded, fitted and integrated into datamodel build on a sql database schema (MySQL). Based on that database, an analytics application is implemented (Streamlit).
*ELT process take 3 hours.*

You can download the raw data from:

https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z

The project is part of the datascientest dataengineering certification.

## Expectation
***
* Creating database
* Creating tables
* Loading compressed file
* Extracting data
* Importing folder games files to db
* Importing folder players files to db
* Transforming data into entity relationship model
* Building views and tables for analyzing the data
* Running an analytics application

### Processflow
![Processflow](https://github.com/philippelerch68/chess365/blob/49ecc8eec75c46d0f2c7ceda8f43931699fe7e7c/db/elt_processflow.png)

### Entity relationship diagram
![ERD](https://github.com/philippelerch68/chess365/blob/main/db/erd_chessdb.png)

### Streamlit dashboard
![Streamlit](https://github.com/philippelerch68/chess365/blob/main/streamlit/images/streamlit.png)

## Modules
***
* ./data/: directory, where the raw data will be stored (created automatically)
* ./db/create_db.py: Creates a database on the MySQL instance
* ./db/create_tables.py: Creates relevent tables on the database
* ./extract_load/extract.py: Download Chess data from the Amazon AWS Cloud and unzip
* ./extract_load/parse_load.py: Process Player and Games files from ./data/ and import to staging tables
* ./statistics/app_insights.py: Analyze data and store results in tables for displaying it later on streamlit application
* ./statistics/app_statistic.py: Retrieve data from tables for global analyze.
* ./statistics/app_views.py: Creating views for data analysis
* ./streamlit/*: Analytics application !! secrets.toml for database authentification !!
* ./transform/parse_datamodel.py: Retreive data from staging and import them in the datamodel (3NF)
* ./tests/test_db.py: define functional tests
* ./config.py: basic configurations
* ./main.py: run the pipeline
* ./config.yaml : basic parameters

### Additional files
Application will generate some files during execution:
* ./insert-error.txt : if integration error append
* ./streamlit/images/game/ *.svg : chess board auto generated on game id request.

## Minimum Requirements
***
Hardware
* Processor: Intel(R) Core(TM) i5-2400S CPU @ 2.50GHz
* Memory: 8GB 
* Operating System: Ubuntu 22.04.1 LTS
* Kernel: Linux 5.15.0-58-generic (x86_64)
* Disk: 120 GB

Software
* Python: Version 3.11 
* MySQL: Version 8.0.32
* requirements.txt

## Run the process
***
Based on an running instance of MySQL, the process will create a database and tables, and loads the chess data from Amazon AWS Cloud. You need to pass the host, user and passwort of your MySQL instance into `config.yaml`. Same issue to use streamlit application (`secrets.toml` for database authentification)
```
$ git clone https://github.com/philippelerch68/chess365.git
$ pip3 install requirements.txt
$ python3 main.py
```
Additionally you can test your environment by running
```
$ python3 -m pytest
```
You can run the streamlit application by
```
$ cd ./streamlit/
$ streamlit run home.py
```

## License
***
GNU General Public License
