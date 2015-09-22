#!/usr/bin/env python
import os
import yaml
from model.TableModel import TableModel
from model.TableFieldModel import TableFieldModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants
class SchemaYamlParser:
    
    def __init__(self , pathToConfigFile = '' , logger=None):
        self._pathToConfigFile = pathToConfigFile
        self.logger = logger
    def listOfTables(self):
        table_model_list = []
        config = ConfigYamlParser(self._pathToConfigFile , self.logger)
        try:
            schema_model_yaml_fileName = config.yamlModelFilePath(YamlConstants.YAMLSCHEMA)
            table_yaml_file = open( schema_model_yaml_fileName , 'rb')
            table_yaml_ingest = table_yaml_file.read()
            table_yaml_file.close()
            for table_yaml_parser in yaml.load_all(table_yaml_ingest):
                tablemodel = TableModel()
                tablemodel.tableName = table_yaml_parser['name']
                tablemodel.fieldsArray = self.listOfTableField(table_yaml_parser['fields'])
                table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.logger.error( '***** SchemaYamlParser.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.logger.error( '***** SchemaYamlParser.listOfTables: Error occured - {0}'.format(str(err)))
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
    
    
    
    

