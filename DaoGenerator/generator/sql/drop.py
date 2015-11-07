import os
from util.constant import JsonConstants
from model.table import TableModel
from model.tablefield import TableFieldModel
from model.view import ViewModel
from jinja2 import Environment , FileSystemLoader

class DropTableViewGenerator(object):
    '''
    This class is charged with generating a SQL script that contains DROP TABLE statements
    '''
    
    def __init__(self , configFileObj=None, deploymentUtil=None , logger = None):
        '''
        Constructor 
        
        @param configFileObj: The parser.config.ConfigJsonParser object passed to this class
        @type configFileObj: parser.config.ConfigJsonParser
        @param deploymentUtil: The deploy.DeploymentUtil object passed to the Generator
        @type deploymentUtil:deploy.DeploymentUtil
        @param logger: The logger object
        @type logger: logger
        '''
        self.__configFileObj = configFileObj
        self.__deploymentUtil = deploymentUtil
        self.__logger = logger
    
    def listOfTables(self):
        '''
        This method converts the JSON dictionary of SQL TABLE properties into a list of model.TableModel objects.
        
        @return: list
        '''
        table_model_list = []
        try:
            for tableObj in self.__configFileObj.sqlTables():
                    tablemodel = TableModel()
                    tablemodel.tableName = tableObj['name']
                    tablemodel.fieldsArray = self.listOfTableField(tableObj['fields'])
                    table_model_list.append(tablemodel)
        except IOError, ioerr:
            self.__logger.error( '***** DropTableViewGenerator.listOfTables: IO Error occured - {0}'.format(str(ioerr)))
        except Exception, err:
            self.__logger.error( '***** DropTableViewGenerator.listOfTables: Error occured - {0}'.format(str(err)))
        return table_model_list
    
    def listOfTableField(self , method_list):
        '''
        This method converts the JSON dictionary of SQL TABLE field properties into a list of model.TableFieldModel objects
        @param method_list: list of fields
        @type method_list: list
        @return: list
        '''
        tableMethodList = []
        for element in method_list:
            field = TableFieldModel()
            field.fieldName = element['field-name']
            field.dataType = element['data-type']
            field.length = element['length']
            field.isPrimaryKey = element['is-primary-key']
            field.autoIncrement = element['auto-increment']
            field.isForeignKeyConstraint = element['is-foreign-key-constraint']
            field.foreignKeyName = element['foreign-key-name']
            field.foreignKeyTable = element['foreign-key-table']
            tableMethodList.append(field)
        return tableMethodList
    
    def listOfViews(self):
        '''
        This method converts the JSON dictionary of SQL VIEW properties into a list of model.ViewModel objects
        
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
        This method sets up the deployment directories, loads the appropriate templates and generates the
        'Drop Tables and Views' script.
        '''
        tableList = []
        viewList = []
        try:
            sql_deployment_directory = self.__configFileObj.deploymentDirectory(JsonConstants.DEPLOYSQL)
            self.__deploymentUtil.createDeploymentDirectory(sql_deployment_directory)
            template_sql_file_name = self.__configFileObj.dropAllTablesAndViewsScriptFileName()
            template_directory = os.path.abspath(self.__configFileObj.templateDirectoryName())
            sql_file_path = sql_deployment_directory +  template_sql_file_name
            tableList = self.listOfTables()
            viewList = self.listOfViews()
            if len(tableList) > 0 or len(viewList) > 0:
                env = Environment(loader=FileSystemLoader(template_directory))
                template = env.get_template(self.__configFileObj.dropTablesAndViewsTemplateFileName())
                template.stream({'schemaName':self.__configFileObj.databaseSchemaName() , 
                                 'databaseName':self.__configFileObj.databaseName() , 
                                 'tableList':tableList,
                                 'viewList':viewList}).dump(sql_file_path)  
        except IOError , ioerror:
            self.__logger.error( '***** DropTableViewGenerator.createSqlFile: IOError occurred - {0}'.format(str(ioerror)))
        except Exception , error:
            self.__logger.error( '***** DropTableViewGenerator.createSqlFile: Error occurred - {0}'.format(str(error)))             