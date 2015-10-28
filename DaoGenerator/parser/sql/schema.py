#!/usr/bin/env python
import os
import json
from model.TableModel import TableModel
from model.TableFieldModel import TableFieldModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants
class SchemaJsonParser:
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    def listOfTables(self):
        table_model_list = []
        config = ConfigJsonParser(self._pathToConfigFile , self.logger)
        try:
            schema_model_json_fileName = config.jsonModelFilePath(JsonConstants.YAMLSCHEMA)
            table_json_file = open( schema_model_json_fileName , 'rb')
            table_json_ingest = table_json_file.read()
            table_json_file.close()
            for table_json_parser in json.load_all(table_json_ingest):
                tablemodel = TableModel()
                tablemodel.tableName = table_json_parser['name']
                tablemodel.fieldsArray = self.listOfTableField(table_json_parser['fields'])
                table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.logger.error( '***** SchemaJsonParser.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.logger.error( '***** SchemaJsonParser.listOfTables: Error occured - {0}'.format(str(err)))
        return table_model_list
    
    def listOfTableField(self , method_list):
        tableMethodList = []
        for element in method_list:
            field = TableFieldModel()
            field.fieldName = element['field-name']
            field.dataType = element['data-type']
            field.length = element['length']
            field.isPrimaryKey = element['is-primary-key']
            field.autoIncrement = element['auto-increment']
            field.isForeignKeyConstraint = element['is-foreign-key-constraint']
            field.foreignKeyName = element['foreign-key-name']
            field.foreignKeyTable = element['foreign-key-table']
            tableMethodList.append(field)
        return tableMethodList
    
    
    
    

