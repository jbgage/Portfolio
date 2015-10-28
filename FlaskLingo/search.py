'''
Created on Oct 12, 2015

@author: jbgage
'''
from elasticsearch import Elasticsearch
import json

class Search(object):
    
    def __init__(self,  propertyObj=None , logger=None):
        self._property = propertyObj
        self._logger = logger
    
    def get(self , term=''):
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
        
        
        
        