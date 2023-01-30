## Table of Contents
1. [General Info](#general-info)
2. [Expectation](#Expectation)
3. [Technologies](#technologies)
4. [Run the process](#Run-the-process)

## General Info
***
The aim of this project is a dataengineering pipeline in the form of an ELT process, which loads chess data of 200 Players and their Gamehistory. The data is loaded, fitted and integrated into datamodel buiild on a sql database schema (MySQL). Later on, an analytics application will be developed based on that database.

![Chess data](https://analyticsengineeringprojects.s3.eu-west-1.amazonaws.com/AE_ChessAnalytics.7z)

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

### Processflow
![Processflow](https://github.com/philippelerch68/chess365/blob/49ecc8eec75c46d0f2c7ceda8f43931699fe7e7c/db/elt_processflow.png)

### Entity relationship diagram
![ERD](https://github.com/philippelerch68/chess365/blob/49ecc8eec75c46d0f2c7ceda8f43931699fe7e7c/db/erd_chessdb.png)

## Modules
***
* ./data/: directory, where the raw data will be stored (created automatically)
* ./db/create_db.py: Creates a database on the MySQL instance
* ./db/create_tables.py: Creates relevent tables on the database
* ./extract_load/extract.py: Download Chess data from the Amazon AWS Cloud and unzip
* ./extract_load/parse_load.py: Process Player and Games files from ./data/ and import to staging tables
* ./transform/parse_datamodel.py: Retreive data from staging and import them in the datamodel (3NF)
* ./tests/test_db.py: define functional tests
* ./config.py: basic configurations
* ./main.py: run the pipeline

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
Based on an running instance of MySQL, the process will create a database and tables, and loads the chess data from Amazon AWS Cloud. You need to pass the host, user and passwort of your MySQL instance into `config.yaml`. 
```
$ git clone https://github.com/philippelerch68/chess365.git
$ pip3 install requirements.txt
$ python3 main.py
```
Additionally you can test your environment by running
```
$ python3 -m pytest
```

## License
***
GNU General Public License