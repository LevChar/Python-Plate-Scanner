# Python Plate Scanner

Simple Python script used for scanning plate numbers, based on OCR API.

Warning : This script only works with **_Python3_**

## Usage
Extract all the files in the repo to a folder of your choice.

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

## Additional Command line arguments:
  `-h, --help`            
shows detailed usage help message

  `-i INPUT, --input INPUT`            
Input directory name
  
  `-d DATABASE, --database DATABASE`            
DataBase Name default is [plate]
  
  `-o OUTPUT, --output OUTPUT`            
  Output file name. If not given, default output is: [STDOUT]
  
  `-l LOG, --log LOG`            
  Log level [0-basic, 1-standard[default], 2-verbose]
  
  `-c CONFIG, --config CONFIG`            
  Configuration file in json format
