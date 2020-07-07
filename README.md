# Python-Plate-Scanner

Simple Python script used for scanning plate numbers, based on OCR API.

Warning : This script only works with **_Python3_**

## Usage
Extract the all the files in the repo to a folder of your choice.

## Simple usage
Run the next command from the same folder where you extracted project's files, 
```
>>> python main.py -i <Input folder name>
```
Please note, `<Input folder name>` should be the name of the folder in which are placed the plate pictures.

## Advanced usage
Read config file to set parameters, **_You can overide (or add for list) any parameters defined inside config.json_**
```
>>> python main.py -c config/config.json
```
