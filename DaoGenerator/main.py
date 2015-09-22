#!/usr/bin/env python
from parser.ConfigYamlParser import ConfigYamlParser
from generator.springmvc.ValueObjectClassGenerator import ValueObjectClassGenerator
from generator.springmvc.DaoClassGenerator import DaoClassGenerator
from generator.springmvc.DaoImplClassGenerator import DaoImplClassGenerator
from generator.sql.SqlTableScriptGenerator import SqlTableScriptGenerator
from generator.sql.SqlViewScriptGenerator import SqlViewScriptGenerator
from generator.sql.SqlStoredProcedureGenerator import SqlStoredProcedureGenerator
from generator.sql.AlterTableScriptGenerator import AlterTableScriptGenerator
from generator.sql.DropTableViewGenerator import DropTableViewGenerator
from generator.sql.DeleteDataScriptGenerator import DeleteDataScriptGenerator
import logging
from logging.config import fileConfig
from optparse import OptionParser
def main(args):
    config = ConfigYamlParser('../config/config.yaml')
    fileConfig('../config/logging.cfg')
    logger = logging.getLogger(__name__)
    parser = OptionParser()
    parser.add_option("-m" , "--mode" , dest = "mode" , help="Mode of operations.")
    (options , args) = parser.parse_args()
    if options.mode is not None | options.mode != '':
        if options.mode == 'generate-table-sql':
            logger.info('Generating table sql scripts...')
            tableSql = SqlTableScriptGenerator(config.configFilePath() , logger)
            tableSql.createSqlFile()
        elif options.mode == 'generate-view-sql':
            logger.info('Generating view sql scripts...')
            viewSql = SqlViewScriptGenerator(config.configFilePath() , logger)
            viewSql.createSqlFile() 
        elif options.mode == 'generate-stored-procedures':
            logger.info('Generating stored procedure scripts...')
            spGen = SqlStoredProcedureGenerator(config.configFilePath() , logger)
            spGen.createSqlFile()
        elif options.mode == 'generate-alter-table-sql':
            logger.info('Generating alter table sql scripts...')
            alterSql = AlterTableScriptGenerator(config.configFilePath() , logger)
            alterSql.generateAlterTableScript()
        elif options.mode == 'generate-delete-table-sql':
            logger.info('Generating delete all data in tables sql scripts...')
            deleteData = DeleteDataScriptGenerator(config.configFilePath() , logger)
            deleteData.generateSqlScript() 
        elif options.mode == 'generate-drop-table-sql':
            logger.info('Generating drop table sql scripts...')
            dropSql = DropTableViewGenerator(config.configFilePath() , logger)
            dropSql.generateSqlScript()
        elif options.mode == 'generate-value-objects':
            logger.info('Generating ValueObject java files...')
            voGen = ValueObjectClassGenerator(config.configFilePath() , logger)   
            voGen.generateInterfaceFiles()
        elif options.mode == 'generate-dao':
            logger.info('Generating DAO interface java files...')
            daoGen = DaoClassGenerator(config.configFilePath() , logger)
            daoGen.generateInterfaceFiles()
        elif options.mode == 'generate-dao-impls':
            logger.info('Generating DAOImpl java files...')
            daoImplGen = DaoImplClassGenerator(config.configFilePath() , logger)
            daoImplGen.generateInterfaceFiles()
    
if __name__ == '__main__':
    main()