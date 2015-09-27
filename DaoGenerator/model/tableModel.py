#!/usr/bin/env python
class TableModel(object):
    
    def __init__(self , tableName = '', fieldsArray = []):
        self._tableName = tableName
        self._fieldsArray = fieldsArray
    
    @property    
    def tableName(self):
        return self._tableName
    
    @tableName.setter
    def tableName(self , value):
        self._tableName = value
    
    @property
    def fieldsArray(self):
        return self._fieldsArray
    
    @fieldsArray.setter    
    def fieldsArray(self , value):
        self._fieldsArray = value
        
        
    def toString(self):
        ls = '\r\n'
        output_string = 'Table Name = ' + self._tableName + ls
        output_string += 'Fields: ' + ls
        for element in self._fieldsArray:
            output_string += '\tField Name = ' + element['fieldName'] + ls
            output_string += '\tDataType = ' + element['dataType'] + ls
            output_string += '\tIs This Field A Primary Key? = ' + str(element['isPrimaryKey']) + ls
            output_string += '\tLength = ' + str(element['length']) + ls
            output_string += '\tDoes this field have a foriegn key constraint? = ' + str(element['isForeignKeyConstraint'])+ ls
            output_string += '\tDoes this field have a foriegn key constraint, and if so, what is the name of the foreign key? = ' + str(element['foreignKeyName']) + ls
            output_string += '\tDoes this field have a foriegn key constraint, and if so, what is the name of the table that contains the foreign key? = ' + str(element['foreignKeyTable']) + ls
        return output_string

    

