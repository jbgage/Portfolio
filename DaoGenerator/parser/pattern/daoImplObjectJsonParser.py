import yaml
from model.DaoImplModel import DaoImplModel
from model.DaoImpMethodModel import DaoImplMethodModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants


class DaoImplObjectYamlParser:
   
    def __init__(self , configFilePath = '' , logger=None):
        self.__configFilePath = configFilePath
        self.logger = logger
    
    def listOfDaoImpls(self):
        daoImplList = []
        yaml_file_name = ''
        config = ConfigYamlParser(self.__configFilePath , self.logger)
        try:
            if not config is None:
                yaml_file_name = config.yamlModelFilePath(YamlConstants.YAMLDAOIMPL)
                yaml_file = open(yaml_file_name , 'rb')
                yaml_file_ingest = yaml_file.read()
                yaml_file.close()
                for yaml_parser in yaml.load_all(yaml_file_ingest):
                    daoImplModel = DaoImplModel()
                    daoImplModel.name = yaml_parser['name']
                    daoImplModel.daoImplemented = yaml_parser['dao-implemented']
                    daoImplModel.comment = yaml_parser['comment']
                    daoImplModel.methodList = self.listOfDaoImplMethods(yaml_parser['methods'])
                    daoImplList.append(daoImplModel)
        except Exception , error:
            self.logger.error( '********** DaoImplObjectYamlParser.listOfDaoImpls: Error occurred - {0}'.format(str(error)))
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
            self.logger.error( '********** DaoImplObjectYamlParser.listOfDaoImplMethods: Error occurred - {0}'.format(str(error)))
        return listOfDaoMethods
        