'''
Created on Sep 27, 2015

@author: bgage
'''
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
    
    def __init__(self, searchEngineUrl='' , dropIndex=False , indexName='' , logger=None):
        self._searchUrl = searchEngineUrl
        self._dropIndexFlag = dropIndex
        self._indexName = indexName
        self.logger = logger
        
        
    def _retrieve_models(self , model_path=''):
        jsonObj = {}
        try:
            if model_path != '':
                abs_path = os.path.abspath(model_path)
                if os.path.isfile(abs_path):
                    with open(abs_path , 'r+') as jsonFile:
                        jsonObj = json.load(jsonFile)
        except IOError , ioerror:
            self.logger.error('SearchEngineIndexer._retrieve_models: IOError occured - {0}'.format(str(ioerror)))  
        except Exception , error:
            self.logger.error('SearchEngineIndexer._retrieve_models: Error occured - {0}'.format(str(error)))
            traceback.print_exc(file=sys.stdout)
        return jsonObj
    
    def _retrieve_models_as_objects(self , model_path='' , type_name=''):
        jsonObj = {}
        try:
            if model_path != '':
                abs_path = os.path.abspath(model_path)
                if os.path.isfile(abs_path):
                    if type_name != '':
                        with open(abs_path , 'r+') as jsonFile:
                                jsonObj = json.load(jsonFile , object_hook=lambda d: namedtuple(type_name , d.keys())(*d.values()))
                    else:
                        jsonObj = self._retrieve_models(model_path)
        except IOError , ioerror:
            self.logger.error('SearchEngineIndexer._retrieve_models_as_objects: IOError occured - {0}'.format(str(ioerror)))  
        except Exception , error:
            self.logger.error('SearchEngineIndexer._retrieve_models_as_objects: Error occured - {0}'.format(str(error)))
            traceback.print_exc(file=sys.stdout)
        return jsonObj
    
    def _recurse_dict(self , target={} , reset_key_val=''):
        d = {}
        for key , val in target.iteritems():
            if isinstance(val , dict):
                d[key] = self._recurse_dict(val , reset_key_val)
            else:
                d[key] = reset_key_val
        return d
    
    def _reinitialize_obj(self , target={} ):
        return self._recurse_dict(target=target , reset_key_val='')
    
    def _create_documents(self , inputFilePath='' , delimiter='' , index_model_path='' , document_model_path=''):
        bulk_data = []
        try:
            index_model = self._retrieve_models(index_model_path)
            doc_model = self._retrieve_models(document_model_path)
            abs_path = os.path.abspath(inputFilePath)
            if os.path.isfile(abs_path):
                with open(abs_path , 'r') as csvObj:
                    csv_file = csv.DictReader(csvObj , delimiter=delimiter , fieldnames=['documentId' , 'documentText'])
                    for row in csv_file:
                        _search_index_model = {}
                        _doc_model = {}
                        _search_index_model = self._reinitialize_obj(index_model)
                        _doc_model = self._reinitialize_obj(doc_model)
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
            self.logger.error('SearchEngineIndexer._create_documents: Error occured - {0}'.format(str(error)))
        return bulk_data
        
    def ingestDataIntoElasticSearchStore(self , 
                                         inputFilePath='' , 
                                         delimiter='' , 
                                         index_model_path='' ,  
                                         document_model_path='' ,
                                         request_model_path='' , 
                                         refresh=True):
        es = None
        request_model = {}
        try:
            es = Elasticsearch(hosts = self._searchUrl)
            request_model = self._retrieve_models(request_model_path)
            if self._dropIndexFlag is True:
                self.logger.info('Dropping Index {0}.'.format(self._indexName))
                es.indices.delete(index=self._indexName)
                self.logger.info('Creating new index...')
                es.indices.create(index=self._indexName , body=request_model)
                bulk_data = self._create_documents(inputFilePath, delimiter, index_model_path , document_model_path)
                es.bulk(index=self._indexName , body=bulk_data , refresh=True)
        except Exception , error:
            self.logger.error('SearchEngineIndexer.ingestDataIntoElasticSearchStore: Error occured - {0}'.format(str(error)))
        