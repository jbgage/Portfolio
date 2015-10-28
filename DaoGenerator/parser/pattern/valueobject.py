#!/usr/bin/env python
import json
from model.VoModel import VoModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants
class ValueObjectJsonParser:
    
    
    def __init__(self , configFilePath = '' , logger=None):
        self.__configFilePath = configFilePath
        self.logger = logger
    def listOfValueObjects(self):
        config = ConfigJsonParser(self.__configFilePath , self.logger)
        voList = []
        try:
            if not config is None:
                vo_json_fileName = config.jsonModelFilePath (JsonConstants.YAMLVALUEOBJECT)
                vo_json_file = open(vo_json_fileName , 'r')
                vo_json_ingest = vo_json_file.read()
                vo_json_file.close()
                for vo_json_parser in json.load_all(vo_json_ingest):
                    vomodel = VoModel()
                    vomodel.modelName = vo_json_parser['name']
                    vomodel.fieldsArray = vo_json_parser['fields']
                    voList.append(vomodel)
        except IOError, ioerr:
            self.logger.error( '********* ValueObjectJsonParser.GetListOfValueObjects: IO Error occurred - {0}'.format(str(ioerr)))
        #except Error, err:
        #    print '********* ValueObjectJsonParser.GetListOfValueObjects: Error occurred - {0}'.format(str(err))
        return voList
    
