#!/usr/bin/env python
import json
from elasticsearch import Elasticsearch

class Search(object):
    '''
    This class is charged with interfacing with Elasticsearch and parsing the resulting response into 
    values that are then passed to the gensim models in the 'topics' module.
    '''
    
    def __init__(self,  propertyObj=None , logger=None):
        '''
        Constructor
        
        @param propertyObj: The property.PropertyUtil object that is passed which contains all of the properties contained in config/application.conf
        @type propertyObj: property.PropertyUtil
        @param logger: logger
        @type logger: logger
        '''
        self._property = propertyObj
        self._logger = logger
    
    def get(self , term=''):
        '''
        This method retrieves the search results returned by Elasticsearch and parses them into a list.
        @param term: The search term
        @type term: str
        @return: list
        '''
        documents = []
        try:
            if self._property is not None:
                elastic_search_url = self._property.elasticSearchUrl
                index_name = self._property.elasticSearchIndexName
                query =  {
                  "query": {
                        "bool": {
                            "must": [
                               {
                                    "query_string": {
                                        "default_field": "document.text",
                                        "query": term
                                    }
                                }
                            ]
                        }
                    }
                 }
                self._logger.info('Query = {0}'.format(query))
                es = Elasticsearch(hosts = elastic_search_url)
                data = es.search(index=index_name , body=query)
                self._logger.info('data = {0}'.format(json.dumps(data)))
                for record in data['hits']['hits']:
                    result = ''
                    result = record['_source']['text']
                    documents.append(result)
        except Exception , error:
            self._logger.error('Search.get: Error occurred - {0}'.format(str(error)))
        return documents