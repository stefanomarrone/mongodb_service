# Mongo Knowledge Base

## Description
This repository is devoted to contain a sample API Python implementation to interface to a MongoDB server. The 
repository serves in particular as a backend for different research project. Each project has a specific set of APIs 
devoted to simplify the interaction with the database.

## Prerequisites
The application relies on the following python packages:
* pydantic
* fastapi
* pymongo
* gridfs
* configparser
* uvicorn

Furthermore, docker must be installed on the machine to properly run the mongodb container.


## Configuring

The **config.ini** file contains the configuration data of the program. A sample of this 
```
[server]
applicationport = 1812 #port of the service
applicationip = 127.0.0.1 #ip address of the service

[mongodb]
address = 127.0.0.1 #address of the mongodb container
port = 27017 #port of the mongodb container

[cosyma]
database = cosyma
product_dbname = products
model_dbname = models

[mat4pat]
database = mat4pat
dbname = repos
```
## Running

To run the program:
1. run a mongodb docker container on the port and on the address written in the configuration. An example command 
   is: **docker run -d -p 27017:27017 mongo**  
2. run the service: **python3 main.py config.ini**

## API description 
* **GET /clean**: clean the database
* **POST /matforpat**: add the structure of the model describing the structure of a system to the repository *products* 
  catalog of the database
  * *configuration_name* - string: name of the configuration
  * file to upload - containing the configuration of the **matforpat** tool to process 
* **GET /matforpat**: retrieve a system model from the *products* catalog of the database
  * *configuration_name* - string: nam of the configuration whose output are to retrieve
* **POST /ddmodels**: add a keras binary model to the *models* catalog of the database
  * *identifier* - integer: identifier of the model
  * *version* - integer: version number of the model
  * file to upload
* **GET /ddmodels**: retrieve a keras binary model from the *models* catalog of the database
  * *identifier* - integer: identifier of the model
  * *version* - integer: version number of the model
* **POST /mbmodels**: add the structure of the model describing the structure of a system to the repository *products* 
  catalog of the database
  * *identifier* - integer: identifier of the model
  * *version* - integer: version number of the model
  * file to upload
* **GET /mbmodels**: retrieve a system model from the *products* catalog of the database
  * *identifier* - integer: identifier of the model
  * *version* - integer: version number of the model

## Projects
The repository has been developed in the context of the **MatForPat** PRIN project. This notwithstanding, the repository can be 
used also for the **Cosyma** project.

## License
The software is licensed under GPL 2.0
