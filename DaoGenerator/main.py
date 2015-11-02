#!/usr/bin/env python
import logging
import sys
import os
from util.configutil import ConfigurationUtil
from util.deployment import DeploymentUtil
from parser.config import ConfigJsonParser
from generator.springmvc.valueobject import ValueObjectClassGenerator
from generator.springmvc.dao import DaoClassGenerator
from generator.springmvc.daoimpl import DaoImplClassGenerator
from generator.sql.table import SqlTableScriptGenerator
from generator.sql.view import SqlViewScriptGenerator
from generator.sql.storedproc import SqlStoredProcedureGenerator
from generator.sql.alter import AlterTableScriptGenerator
from generator.sql.drop import DropTableViewGenerator
from generator.sql.delete import DeleteDataScriptGenerator
from logging.config import fileConfig
from optparse import OptionParser

def main(args):
    fileConfig('config/logging.cfg')
    logger = logging.getLogger(__name__)
    configUtil = ConfigurationUtil('config/config.json' , logger)
    config = ConfigJsonParser(configUtil.createConfigurationObject() , logger)
    deploy = DeploymentUtil(logger)
    parser = OptionParser()
    parser.add_option("-m" , "--mode" , dest = "mode" , help="Mode of operations.")
    (options , args) = parser.parse_args()
    if options.mode is not None and options.mode != '':
        if options.mode == 'generate-table-sql':
            logger.info('Generating table sql scripts...')
            tableSql = SqlTableScriptGenerator(config , deploy ,logger)
            tableSql.createSqlFile()
        elif options.mode == 'generate-view-sql':
            logger.info('Generating view sql scripts...')
            viewSql = SqlViewScriptGenerator(config , deploy ,logger)
            viewSql.createSqlFile() 
        elif options.mode == 'generate-stored-procedures':
            logger.info('Generating stored procedure scripts...')
            spGen = SqlStoredProcedureGenerator(config , deploy ,logger)
            spGen.createSqlFile()
        elif options.mode == 'generate-alter-table-sql':
            logger.info('Generating alter table sql scripts...')
            alterSql = AlterTableScriptGenerator(config , deploy , logger)
            alterSql.generateAlterTableScript()
        elif options.mode == 'generate-delete-table-sql':
            logger.info('Generating delete all data in tables sql scripts...')
            deleteData = DeleteDataScriptGenerator(config , deploy , logger)
            deleteData.generateSqlScript() 
        elif options.mode == 'generate-drop-table-sql':
            logger.info('Generating drop table sql scripts...')
            dropSql = DropTableViewGenerator(config , deploy ,logger)
            dropSql.generateSqlScript()
        elif options.mode == 'generate-value-objects':
            logger.info('Generating ValueObject java files...')
            voGen = ValueObjectClassGenerator(config , deploy ,logger)   
            voGen.generateClassFiles()
        elif options.mode == 'generate-dao':
            logger.info('Generating DAO interface java files...')
            daoGen = DaoClassGenerator(config , deploy ,logger)
            daoGen.generateInterfaceFiles()
        elif options.mode == 'generate-dao-impls':
            logger.info('Generating DAOImpl java files...')
            daoImplGen = DaoImplClassGenerator(config , deploy ,logger)
            daoImplGen.generateClassFiles()
    
if __name__ == '__main__':
    main(sys.argv)