#!/usr/bin/env python
from model.dao import DaoModel
from model.daomethod import DaoMethodModel
from parser.config import ConfigJsonParser
from parser.constant import JsonConstants

class DaoObjectJsonParser(object):
    
    def __init__(self , configFileObject = None , logger=None):
        self.__configFileObject = configFileObject
        self.__logger = logger
    
    def listOfDaos(self):
        daoList = []
        try:
            for daoModelObj in self.__configFileObject.daos():
                daoModel = DaoModel()
                daoModel.name = daoModelObj['name']
                daoModel.comment = daoModelObj['comment']
                daoModel.methodList = self.listOfDaoMethods(daoModelObj['methods'])
                daoList.append(daoModel)
        except Exception , error:
            self.__logger.error( '**************** DaoObjectJsonParser.listOfDaos(): Error occurred - {0}'.format(str(error)))
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
            self.__logger.error( '**************** DaoObjectJsonParser.listOfDaoMethods(): Error occurred - {0}'.format(str(error)))
        return daoMethodList