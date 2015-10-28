#!/usr/bin/env python
import json
from model.StoredProcedureModel import StoredProcedureModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants

class StoredProcedureJsonParser:
    
    def __init__(self , pathToJsonConfigFile , logger=None):
        self._pathToJsonConfigFile = pathToJsonConfigFile
        self.logger = logger
    def listOfStoredProcedures(self):
        json_ingest = None
        json_file = None
        sp_list = []
        json_file_name = ''
        config = ConfigJsonParser(self._pathToJsonConfigFile , self.logger)
        try:
            json_file_name = config.jsonModelFilePath(JsonConstants.YAMLSTOREDPROCEDURES)
            json_file = open(json_file_name , 'rb')
            json_ingest = json_file.read()
            json_file.close()
            if not json_ingest is None:
                for json_parser in json.load_all(json_ingest):
                    sp = StoredProcedureModel()
                    sp.name = json_parser['name']
                    sp.tableName = json_parser['table-name']
                    sp.storedProcedureType = json_parser['stored-procedure-type']
                    sp.viewName = json_parser['view-name']
                    sp.inputVariables = json_parser['input-variables']
                    sp.outputVariables = json_parser['output-variables']
                    sp.selectStatementFields = json_parser['select-statement-fields']
                    sp.insertStatementFields = json_parser['insert-statement-fields']
                    sp.updateStatementFields = json_parser['update-statement-fields']
                    sp.whereClause = json_parser['where-clause']
                    sp_list.append(sp)
        except IOError , ioerr:
            self.logger.error( '****** StoredProcedureJsonParser.listOfStoredProcedures: IOError occurred - {0}'.format(str(ioerr)))
        return sp_list
