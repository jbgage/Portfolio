#!/usr/bin/env python
import jsonutil
import os

class ConfigurationUtil(object):
    
    def __init__(self, configurationFilePath='' , logger=None):
        self._configFilePath = configurationFilePath
        self.logger = logger
    
    def createConfigurationObject(self):
        configObj = {}
        jsonConfig = {}
        jsonUtil = None
        try:
            confAbsPath = os.path.abspath(self._configFilePath)
            if confAbsPath is not None:
                jsonUtil = jsonutil.JsonUtil(confAbsPath)
                if jsonUtil is not None:
                    jsonConfig = jsonUtil.retrieveJsonObjectFromJsonConfig()
                    if jsonConfig is not None and len(jsonConfig) > 0:
                        configObj['main-config'] = jsonConfig
                        configObj['models'] = jsonConfig['jsonModelFiles']
                        configDir = jsonConfig['directories']['config']
                        configObj['profile'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir + configObj['models']['profile'])
                        configObj['database'] = {}
                        configObj['database']['views'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir +  configObj['models']['database']['view'])
                        configObj['database']['schema'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath(configDir +  configObj['models']['database']['schema'])
                        configObj['database']['stored-procedures'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir +  configObj['models']['database']['storedProcedures'])
                        configObj['persistence'] = {}
                        configObj['persistence']['dao'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir +  configObj['models']['persistence']['dao'])
                        configObj['persistence']['dao-impl'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir +  configObj['models']['persistence']['daoImpl'])
                        configObj['persistence']['dao-factory'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath( configDir +  configObj['models']['persistence']['daoFactory'])
                        configObj['value-object'] = jsonUtil.retrieveJsonObjectFromJsonConfigPath(configDir +  configObj['models']['valueObject'])
        except IOError , ioerror:
            self.logger.error("ConfigurationUtil.createConfigurationObject: IOException occurred - {0}".format(str(ioerror)))
        except Exception , error:
            self.logger.error("ConfigurationUtil.createConfigurationObject: Exception occurred - {0}".format(str(error)))
        return configObj