#!/usr/bin/env python
import json
import os
import csv
import traceback
import sys
from collections import namedtuple
from collections import Mapping
from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers

class SearchEngineIndexer(object):
    '''
    This is a utility class that handles the indexation of the resulting novel text (from the TextGenerator object) into the target
    search engine 'store', which in the case of this project, is Elasticsearch.
    '''
    
    def __init__(self, searchEngineUrl='' , dropIndex=False , indexName='' , logger=None):
        '''
        Constructor
        
        @param searchEngineUrl: The indexation url to the search engine; for Elasticsearch, this is usually http://localhost:9200
        @type searchEngineUrl: string
        @param dropIndex: Flag as to whether the associated index should be dropped 
        @type dropIndex: boolean
        @param indexName: The name of the search index
        @type indexName: str
        @param logger: The logger object
        @type logger: logger
        '''
        self._searchUrl = searchEngineUrl
        self._dropIndexFlag = dropIndex
        self._indexName = indexName
        self.logger = logger
        
    def __retrieve_models(self , model_path=''):
        '''
        This method retrieves JSON-formatted files that will be used during the indexation process. This 
        method was created to preclude the need to have in-line JSON in the code, so this helper method was
        devised. These JSON files are the config/ directory.
        
        @param model_path: The relative path to the model file(s)
        @type model_path: str
        @return: dict
        '''
        jsonObj = {}
        try:
            if model_path != '':
                abs_path = os.path.abspath(model_path)
                if os.path.isfile(abs_path):
                    with open(abs_path , 'r+') as jsonFile:
                        jsonObj = json.load(jsonFile)
        except IOError , ioerror:
            self.logger.error('SearchEngineIndexer.__retrieve_models: IOError occured - {0}'.format(str(ioerror)))  
        except Exception , error:
            self.logger.error('SearchEngineIndexer.__retrieve_models: Error occured - {0}'.format(str(error)))
            traceback.print_exc(file=sys.stdout)
        return jsonObj
    
    def __retrieve_models_as_objects(self , model_path='' , type_name=''):
        '''
        This is a helper method to aid in the retrieval of the JSON model files as either a JSON object or a series of tuples.
        
        @param model_path: The relative path to the model files.
        @type model_path: str
        @param type_name: The 'type' of object. 
        @type type_name: str
        @return: dict
        '''
        jsonObj = {}
        try:
            if model_path != '':
                abs_path = os.path.abspath(model_path)
                if os.path.isfile(abs_path):
                    if type_name != '':
                        with open(abs_path , 'r+') as jsonFile:
                                jsonObj = json.load(jsonFile , object_hook=lambda d: namedtuple(type_name , d.keys())(*d.values()))
                    else:
                        jsonObj = self.__retrieve_models(model_path)
        except IOError , ioerror:
            self.logger.error('SearchEngineIndexer.__retrieve_models_as_objects: IOError occured - {0}'.format(str(ioerror)))  
        except Exception , error:
            self.logger.error('SearchEngineIndexer.__retrieve_models_as_objects: Error occured - {0}'.format(str(error)))
            traceback.print_exc(file=sys.stdout)
        return jsonObj
    
    def __recurse_dict(self , target={} , reset_key_val=''):
        '''
        This method is used to reset the keys of a given dictionary object to the same value. It
        is primarily used to reset all of the values in the dictionary objects that are initially 
        created during the initial indexation processes.
         
        @param target: The dictionary object that is recursed through in order to 'reset' the values of the keys.
        @type target: dict
        @param reset_key_val: The value all keys in 'target' are set to.
        @type reset_key_val: str
        @return: dict
        '''
        d = {}
        for key , val in target.iteritems():
            if isinstance(val , dict):
                d[key] = self.__recurse_dict(val , reset_key_val)
            else:
                d[key] = reset_key_val
        return d
    
    def __reinitialize_obj(self , target={} ):
        '''
        This is a utility method used to set all the keys of the 'target' dictionary to ''.
        
        @param target: The dictionary to 'reset'.
        @type target: dict
        @return: dict
        '''
        return self.__recurse_dict(target=target , reset_key_val='')
    
    def __create_documents(self , inputFilePath='' , delimiter='' , index_model_path='' , document_model_path=''):
        '''
        This method is charged with creating Elasticsearch documents.
        
        @param inputFilePath: The path to the CSV file
        @type inputFilePath: str
        @param delimiter: The delimiter used in the CSV file
        @type delimiter: str
        @param index_model_path: The path to the 'index.model.json' file.
        @type index_model_path: str
        @param document_model_path: The path to the 'document.model.json' file.
        @type document_model_path: str
        @return: list
        '''
        bulk_data = []
        try:
            index_model = self.__retrieve_models(index_model_path)
            doc_model = self.__retrieve_models(document_model_path)
            abs_path = os.path.abspath(inputFilePath)
            if os.path.isfile(abs_path):
                with open(abs_path , 'r') as csvObj:
                    csv_file = csv.DictReader(csvObj , delimiter=delimiter , fieldnames=['documentId' , 'documentText'])
                    for row in csv_file:
                        _search_index_model = {}
                        _doc_model = {}
                        _search_index_model = self.__reinitialize_obj(index_model)
                        _doc_model = self.__reinitialize_obj(doc_model)
                        _search_index_model['index']['_index'] = self._indexName
                        _search_index_model['index']['_id'] = row['documentId']
                        _search_index_model['index']['_type'] = 'document'
                        _doc_model['text'] = row['documentText']
                        _doc_model['timestamp'] = datetime.now()
                        bulk_data.append(_search_index_model)
                        bulk_data.append(_doc_model)
            else:
                self.logger.error('There was an error retrieving the CSV file via the passed parameters. Please verify accuracy of path.')    
        except Exception , error:
            self.logger.error('SearchEngineIndexer.__create_documents: Error occured - {0}'.format(str(error)))
        return bulk_data
    
    def ingestDataIntoElasticSearchStore(self , 
                                         inputFilePath='' , 
                                         delimiter='' , 
                                         index_model_path='' ,  
                                         document_model_path='' ,
                                         request_model_path='' , 
                                         refresh=True):
        '''
        This method is charged with indexing the documents created above via Elasticsearch's Bulk API
        
        @param inputFilePath: The path to the CSV file
        @type inputFilePath: str
        @param delimiter: The delimiter used in the CSV file
        @type delimiter: str
        @param index_model_path: The path to the 'index.model.json' file.
        @type index_model_path: str
        @param document_model_path: The path to the 'document.model.json' file.
        @type document_model_path: str
        @param request_model_path: The path to the 'search.engine.model.json' file
        @type request_model_path: str
        @param refresh: A flag to determine if the index should be refreshed.
        @type refresh: bool
        '''
        es = None
        request_model = {}
        try:
            es = Elasticsearch(hosts = self._searchUrl)
            request_model = self.__retrieve_models(request_model_path)
            if self._dropIndexFlag is True:
                self.logger.info('Dropping Index: \'{0}\'.'.format(self._indexName))
                es.indices.delete(index=self._indexName)
                self.logger.info('Creating new index...')
                es.indices.create(index=self._indexName , body=request_model)
                bulk_data = self.__create_documents(inputFilePath, delimiter, index_model_path , document_model_path)
                es.bulk(index=self._indexName , body=bulk_data , refresh=True)
        except Exception , error:
            self.logger.error('SearchEngineIndexer.ingestDataIntoElasticSearchStore: Error occured - {0}'.format(str(error)))