#!/usr/bin/env python
from ConfigParser import ConfigParser

class PropertyUtil(object):
    
    '''
    This class reads in properties contained in the project's configuration file and
    allows different components to access the values defined in said file.
    '''
    def __init__(self, configFilePath=''):
        '''
        Constructor
        '''
        self._configFilePath=configFilePath
        self._parser=ConfigParser()
        self._parser.read(self._configFilePath)
        
    def _getstr(self , section='' , property_name=''):
        return self._parser.get(section , property_name)
    
    def _getbool(self , section='' , property_name=''):
        return self._parser.getboolean(section , property_name)
    
    def _getint(self , section='' , property_name=''):
        return self._parser.getint(section, property_name)
    
    @property
    def elasticSearchUrl(self):
        return self._getstr('ElasticSearch_Parameters' , 'elastic.search.qualified.url')
    
    @property
    def elasticSearchIndexName(self):
        return self._getstr('ElasticSearch_Parameters' , 'elastic.search.indexname')