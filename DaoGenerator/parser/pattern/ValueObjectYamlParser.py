#!/usr/bin/env python
import yaml
from model.VoModel import VoModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants
class ValueObjectYamlParser:
    
    
    def __init__(self , configFilePath = '' , logger=None):
        self.__configFilePath = configFilePath
        self.logger = logger
    def listOfValueObjects(self):
        config = ConfigYamlParser(self.__configFilePath , self.logger)
        voList = []
        try:
            if not config is None:
                vo_yaml_fileName = config.yamlModelFilePath (YamlConstants.YAMLVALUEOBJECT)
                vo_yaml_file = open(vo_yaml_fileName , 'r')
                vo_yaml_ingest = vo_yaml_file.read()
                vo_yaml_file.close()
                for vo_yaml_parser in yaml.load_all(vo_yaml_ingest):
                    vomodel = VoModel()
                    vomodel.modelName = vo_yaml_parser['name']
                    vomodel.fieldsArray = vo_yaml_parser['fields']
                    voList.append(vomodel)
        except IOError, ioerr:
            self.logger.error( '********* ValueObjectYamlParser.GetListOfValueObjects: IO Error occurred - {0}'.format(str(ioerr)))
        #except Error, err:
        #    print '********* ValueObjectYamlParser.GetListOfValueObjects: Error occurred - {0}'.format(str(err))
        return voList
    
