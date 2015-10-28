import json
from model.DaoImplModel import DaoImplModel
from model.DaoImpMethodModel import DaoImplMethodModel
from parser.ConfigJsonParser import ConfigJsonParser
from parser.constants import JsonConstants


class DaoImplObjectJsonParser:
   
    def __init__(self , configFilePath = '' , logger=None):
        self.__configFilePath = configFilePath
        self.logger = logger
    
    def listOfDaoImpls(self):
        daoImplList = []
        json_file_name = ''
        config = ConfigJsonParser(self.__configFilePath , self.logger)
        try:
            if not config is None:
                json_file_name = config.jsonModelFilePath(JsonConstants.YAMLDAOIMPL)
                json_file = open(json_file_name , 'rb')
                json_file_ingest = json_file.read()
                json_file.close()
                for json_parser in json.load_all(json_file_ingest):
                    daoImplModel = DaoImplModel()
                    daoImplModel.name = json_parser['name']
                    daoImplModel.daoImplemented = json_parser['dao-implemented']
                    daoImplModel.comment = json_parser['comment']
                    daoImplModel.methodList = self.listOfDaoImplMethods(json_parser['methods'])
                    daoImplList.append(daoImplModel)
        except Exception , error:
            self.logger.error( '********** DaoImplObjectJsonParser.listOfDaoImpls: Error occurred - {0}'.format(str(error)))
        return daoImplList
        
    def listOfDaoImplMethods(self , methodList):
        listOfDaoMethods = []
        try:
            if not methodList is None and len(methodList) > 0:
                for element in methodList:
                    implMethod = DaoImplMethodModel()
                    implMethod.methodName = element['method-name']
                    implMethod.comment = element['comment']
                    implMethod.valueObjectType = element['value-object-type']
                    implMethod.returnType = element['return-type']
                    implMethod.methodInputVariables = element['method-input-variables']
                    implMethod.storedProcedureName = element['stored-procedure-name']
                    implMethod.sqlCommandObjectInputVariables = element['sql-command-object-input-variables']
                    implMethod.resultSetParameters = element['result-set-parameters']
                    listOfDaoMethods.append(implMethod)
        except Exception , error:
            self.logger.error( '********** DaoImplObjectJsonParser.listOfDaoImplMethods: Error occurred - {0}'.format(str(error)))
        return listOfDaoMethods
        