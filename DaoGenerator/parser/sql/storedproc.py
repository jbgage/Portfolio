#!/usr/bin/env python
import json
from model.storedproc import StoredProcedureModel
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants
class StoredProcedureJsonParser:
    def __init__(self , configFileObj=None , logger=None):
        self.__configFileObj = configFileObj
        self.__logger = logger
    def listOfStoredProcedures(self):
        sp_list = []
        try:
            if not self.__configFileObj is None:
                for spObj in self.__configFileObj.sqlStoredProcedures():
                    sp = StoredProcedureModel()
                    sp.name = spObj['name']
                    sp.tableName = spObj['table-name']
                    sp.storedProcedureType = spObj['stored-procedure-type']
                    sp.viewName = spObj['view-name']
                    sp.inputVariables = spObj['input-variables']
                    sp.outputVariables = spObj['output-variables']
                    sp.selectStatementFields = spObj['select-statement-fields']
                    sp.insertStatementFields = spObj['insert-statement-fields']
                    sp.updateStatementFields = spObj['update-statement-fields']
                    sp.whereClause = spObj['where-clause']
                    sp_list.append(sp)
        except IOError , ioerr:
            self.__logger.error( '****** StoredProcedureJsonParser.listOfStoredProcedures: IOError occurred - {0}'.format(str(ioerr)))
        return sp_list
