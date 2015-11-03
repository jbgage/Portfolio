#!/usr/bin/env python
from model.table import TableModel
from model.tablefield import TableFieldModel

class SchemaJsonParser(object):
    '''
    This class is charged with assembling the different values to create TABLE-specific SQL command 
    script types (e.g. 'CREATE TABLE' , 'ALTER TABLE', 'DROP TABLE')
    '''
    
    def __init__(self , configFileObj = None , logger=None):
        '''
        Constructor 
        
        @param configFileObject: The configuration object that is passed to this class
        @type configFileObject: config.ConfigJsonParser
        @param logger: logger
        @type logger: logger
        '''
        self.__configFileObj = configFileObj
        self.__logger = logger
    
    def listOfTables(self):
        table_model_list = []
        try:
            for tableObj in self.__configFileObj.sqlTables():
                    tablemodel = TableModel()
                    tablemodel.tableName = tableObj['name']
                    tablemodel.fieldsArray = self.listOfTableField(tableObj['fields'])
                    table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.__logger.error( '***** SchemaJsonParser.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.__logger.error( '***** SchemaJsonParser.listOfTables: Error occured - {0}'.format(str(err)))
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