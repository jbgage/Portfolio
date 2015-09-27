#!/usr/bin/env python
import yaml
from model.StoredProcedureModel import StoredProcedureModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants

class StoredProcedureYamlParser:
    
    def __init__(self , pathToYamlConfigFile , logger=None):
        self._pathToYamlConfigFile = pathToYamlConfigFile
        self.logger = logger
    def listOfStoredProcedures(self):
        yaml_ingest = None
        yaml_file = None
        sp_list = []
        yaml_file_name = ''
        config = ConfigYamlParser(self._pathToYamlConfigFile , self.logger)
        try:
            yaml_file_name = config.yamlModelFilePath(YamlConstants.YAMLSTOREDPROCEDURES)
            yaml_file = open(yaml_file_name , 'rb')
            yaml_ingest = yaml_file.read()
            yaml_file.close()
            if not yaml_ingest is None:
                for yaml_parser in yaml.load_all(yaml_ingest):
                    sp = StoredProcedureModel()
                    sp.name = yaml_parser['name']
                    sp.tableName = yaml_parser['table-name']
                    sp.storedProcedureType = yaml_parser['stored-procedure-type']
                    sp.viewName = yaml_parser['view-name']
                    sp.inputVariables = yaml_parser['input-variables']
                    sp.outputVariables = yaml_parser['output-variables']
                    sp.selectStatementFields = yaml_parser['select-statement-fields']
                    sp.insertStatementFields = yaml_parser['insert-statement-fields']
                    sp.updateStatementFields = yaml_parser['update-statement-fields']
                    sp.whereClause = yaml_parser['where-clause']
                    sp_list.append(sp)
        except IOError , ioerr:
            self.logger.error( '****** StoredProcedureYamlParser.listOfStoredProcedures: IOError occurred - {0}'.format(str(ioerr)))
        return sp_list
