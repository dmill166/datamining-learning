# Homework 01

## XLSX Parse to JSON

## Goal

To illustrate how to perform a typical XLSX parse to JSON

## Instructions 

In this assignment you are NOT allowed to use any external library to read the given XLSX file directly. Instead, you should unzip the XLSX file and extract the following XML files: sharedStrings.xml and sheet1.xml. To be clear, after unzipping athletes.xlsx you should see the following file structure: 

```
Archive:  Athletes.xlsx
  [Content_Types].xml     
  _rels/.rels             
  xl/_rels/workbook.xml.rels  
  xl/workbook.xml         
  xl/sharedStrings.xml    
  xl/theme/theme1.xml     
  xl/styles.xml          
  xl/worksheets/sheet1.xml  
  docProps/core.xml       
  docProps/app.xml
```

The shared strings file should be read first and be used to create a list of all strings referenced in the document. You should then read sheet1.xml and extract all of its rows. Note that the content of each cell maps to the index in the shared string list. Finally, your parser should then saved the extracted information in json, using the format below: 

```
[
    {"name": "AALERUD Katrine", "noc": "Norway", "discipline": "Cycling Road"}, 
    {"name": "ABAD Nestor", "noc": "Spain", "discipline": "Artistic Gymnastics"}, 
    {"name": "ABAGNALE Giovanni", "noc": "Italy", "discipline": "Rowing"},
    ...
]
```

Hint: use the "xml" parser from beautiful soup. 