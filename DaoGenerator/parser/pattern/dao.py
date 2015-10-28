
import json
from model.DaoModel import DaoModel
from model.DaoMethodModel import DaoMethodModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants

class DaoObjectJsonParser(object):
    
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    def listOfDaos(self):
        daoList = []
        config = ConfigJsonParser(self._configFilePath , self.logger)
        try:
            dao_file_name = config.jsonModelFilePath(JsonConstants.YAMLDAO)
            dao_file = open(dao_file_name , 'rb')
            dao_file_ingest = dao_file.read()
            dao_file.close() 
            for json_parser in json.load_all(dao_file_ingest):
                daoModel = DaoModel()
                daoModel.name = json_parser['name']
                daoModel.comment = json_parser['comment']
                daoModel.methodList = self.listOfDaoMethods(json_parser['methods'])
                daoList.append(daoModel)
        except Exception , error:
            self.logger.error( '**************** DaoObjectJsonParser.listOfDaos(): Error occurred - {0}'.format(str(error)))
        return daoList
        
    def listOfDaoMethods(self , method_list):
        daoMethodList = []
        try:
            for element in method_list:
                daoMethodModel = DaoMethodModel()
                daoMethodModel.methodName = element['method-name']
                daoMethodModel.returnType = element['return-type']
                daoMethodModel.inputVariables = element['input-variables']
                daoMethodList.append(daoMethodModel)
        except Exception , error:
            self.logger.error( '**************** DaoObjectJsonParser.listOfDaoMethods(): Error occurred - {0}'.format(str(error)))
        return daoMethodList
        
        