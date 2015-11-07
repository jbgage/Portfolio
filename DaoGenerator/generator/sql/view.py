#!/usr/bin/env python
import os
from jinja2 import Environment , FileSystemLoader
from util.constant import JsonConstants
from model.view import ViewModel

class SqlViewScriptGenerator(object):
    '''
    This class is charged with creating a SQL script that contains CREATE VIEW statements.
    '''
    
    def __init__(self , config=None , deploymentUtil=None ,  logger=None):
        '''
        Constructor 
        
        @param config: The parser.config.ConfigJsonParser object passed to this class
        @type config: parser.config.ConfigJsonParser
        @param deploymentUtil: The deploy.DeploymentUtil object passed to the Generator
        @type deploymentUtil:deploy.DeploymentUtil
        @param logger: The logger object
        @type logger: logger
        '''
        self.__configFileObj = config
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
        
    def listOfViews(self):
        '''
        This method converts the JSON dictionary of SQL VIEW properties into a list of ViewModel objects
        
        @return: list
        '''
        view_list = []
        try:
            for viewObj in self.__configFileObj.sqlViews():
                viewModel = ViewModel()
                viewModel.viewName = viewObj['name']
                viewModel.selectClause = viewObj['select-clause']
                viewModel.fromClause = viewObj['from-clause']
                viewModel.whereClause = viewObj['where-clause']
                view_list.append(viewModel)
        except IOError, ioerr:
            self.__logger.error( '***** ViewJsonParser.listOfViews: IO Error occured - {0}'.format(str(ioerr)))
        return view_list
        
    
        
    def createSqlFile(self):
        '''
        This method retrieves the template file from the util.ConfigurationProperties and creates the 'Create Views' SQL script.
        '''
        sql_file_name = ''
        sql_directory = ''
        sql_file_path = ''
        view_list = []
        try:
            if not self.__configFileObj is None:
                view_list = self.listOfViews()
                sql_file_name = self.__configFileObj.createViewsScriptFileName()
                sql_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
                self.__deploymentUtil.createDeploymentDirectory(sql_directory)
                template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
                if len(view_list) > 0:
                    env = Environment(loader=FileSystemLoader(template_directory))
                    template = env.get_template(self.__configFileObj.createViewsTemplateFileName())
                    sql_file_path = sql_directory +  sql_file_name
                    template.stream({'schemaName':self.__configFileObj.databaseSchemaName() , 
                                     'databaseName':self.__configFileObj.databaseName() , 
                                     'viewList':view_list}).dump(sql_file_path)               
        except IOError, ioerror:
            self.__logger.error( '***** SqlViewScriptGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        except Exception, error:
            self.__logger.error( '***** SqlViewScriptGenerator.createSqlFile: Error occurred - {0}'.format(str(error)))