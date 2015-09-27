
import yaml
from model.DaoModel import DaoModel
from model.DaoMethodModel import DaoMethodModel
from parser.ConfigYamlParser import ConfigYamlParser
from parser.YamlConstants import YamlConstants

class DaoObjectYamlParser(object):
    
    def __init__(self , configFilePath = '' , logger=None):
        self._configFilePath = configFilePath
        self.logger = logger
    def listOfDaos(self):
        daoList = []
        config = ConfigYamlParser(self._configFilePath , self.logger)
        try:
            dao_file_name = config.yamlModelFilePath(YamlConstants.YAMLDAO)
            dao_file = open(dao_file_name , 'rb')
            dao_file_ingest = dao_file.read()
            dao_file.close() 
            for yaml_parser in yaml.load_all(dao_file_ingest):
                daoModel = DaoModel()
                daoModel.name = yaml_parser['name']
                daoModel.comment = yaml_parser['comment']
                daoModel.methodList = self.listOfDaoMethods(yaml_parser['methods'])
                daoList.append(daoModel)
        except Exception , error:
            self.logger.error( '**************** DaoObjectYamlParser.listOfDaos(): Error occurred - {0}'.format(str(error)))
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
            self.logger.error( '**************** DaoObjectYamlParser.listOfDaoMethods(): Error occurred - {0}'.format(str(error)))
        return daoMethodList
        
        