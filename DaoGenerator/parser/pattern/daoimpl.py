#!/usr/bin/env python
from model.daoimpl import DaoImplModel
from model.daoimplmethod import DaoImplMethodModel

class DaoImplObjectJsonParser(object):
    '''
    This class is charged with assembling the different values used to generate DAOImpl classes.
    '''
    
    def __init__(self , configFileObject = None , logger=None):
        '''
        Constructor
        
        @param configFileObject: The configuration object that is passed to this class
        @type configFileObject: config.ConfigJsonParser
        @param logger: logger
        @type logger: logger
        '''
        self.__configFileObj = configFileObject
        self.__logger = logger
    
    def listOfDaoImpls(self):
        daoImplList = []
        json_file_name = ''
        try:
            if self.__configFileObj is not None:
                for daoImplObj in self.__configFileObj.daoImpls():
                    daoImplModel = DaoImplModel()
                    daoImplModel.name = daoImplObj['name']
                    daoImplModel.daoImplemented = daoImplObj['dao-implemented']
                    daoImplModel.comment = daoImplObj['comment']
                    daoImplModel.methodList = self.listOfDaoImplMethods(daoImplObj['methods'])
                    daoImplList.append(daoImplModel)
        except Exception , error:
            self.__logger.error( '********** DaoImplObjectJsonParser.listOfDaoImpls: Error occurred - {0}'.format(str(error)))
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
            self.__logger.error( '********** DaoImplObjectJsonParser.listOfDaoImplMethods: Error occurred - {0}'.format(str(error)))
        return listOfDaoMethods       