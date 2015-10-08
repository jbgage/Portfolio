#!/usr/bin/env python
class VoModel(object):
    
    def __init__(self , modelName = '', fieldsArray = []):
        self._modelName = modelName
        self._fieldsArray = fieldsArray
     
    @property    
    def modelName(self):
        return self._modelName
    
    @modelName.setter
    def modelName(self , value):
        self._modelName = value
    
    @property   
    def fieldsArray(self):
        return self._fieldsArray
    
    @fieldsArray.setter
    def fieldsArray(self , value):
        self._fieldsArray = value
        
    def toString(self):
        ls = '\r\n'
        string_output = 'Model Name = ' + self._modelName + ls
        
        string_output += 'Fields: ' + ls
        for element in self._fieldsArray:
            string_output += '\tField Name = ' + element['fieldName'] + ls
            string_output += '\tData Type = ' + element['dataType'] + ls
        return string_output

