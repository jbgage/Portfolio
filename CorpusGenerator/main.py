'''
Created on Sep 27, 2015

@author: bgage
'''
import os
import sys
import logging
import nltk
import urllib2
import uuid
import traceback
from generator import TextGenerator
from property import PropertyUtil
from indexer import SearchEngineIndexer
from logging.config import fileConfig

def _load_nltk_data(file_path='' , prefix='' ):
    return nltk.data.load(file_path[len(prefix):] )

def _load_nltk_data_as_string(file_path='' , prefix='' ):
    return nltk.data.load(file_path[len(prefix):] , format='text' )

def _load_url_data(url=''):
    response = urllib2.urlopen(url)
    return response.read()

def _load_local_file(file_path='' ):
    data = ''
    if os.path.isfile(file_path):
        with open(file_path) as local_file:
            data = local_file.read()
    return data

def _create_property_dict(properties=None):
    property_dict = {}
    property_dict['engine-type'] = properties.corpusEngineType
    property_dict['corpora-ref-path-type'] = properties.corporaReferencePathType
    property_dict['corpora-ref-path'] = properties.corporaReferencePath
    property_dict['data-file-record-num'] = properties.dataFileRecordNumber
    property_dict['generate-uuids'] = properties.isGenerateUuids
    property_dict['words-per-sentence'] = properties.wordsPerSentence
    property_dict['sentences-per-record'] = properties.sentencesPerRecord
    property_dict['output-file-path'] = properties.dataFileOutputPath
    property_dict['datafile-delimiter'] = properties.dataFileDelimiter
    property_dict['search-engine-url'] = properties.elasticSearchUrl
    property_dict['search-index-name'] = properties.elasticSearchIndexName
    property_dict['drop-index-flag'] = properties.isDropIndex
    property_dict['is-datafile-to-be-generated'] = properties.isOperationGenerateDatafile
    property_dict['is-datafile-to-be-indexed'] = properties.isOperationIndexDataFile
    return property_dict

def _generate_array_of_records(text_generator=None , 
                               engine_type='' , 
                               bGenerateUuids=True , 
                               corpus='' , 
                               number_of_words_per_sentence=0 , 
                               number_of_sentences_per_record=0 , 
                               number_of_records=0):
    data_obj = []
    if engine_type == 'direct':
        data_obj = text_generator.generate_direct_text(number_of_sentences_per_record , number_of_records)
    elif engine_type == 'hiddenmarkovmodel':
        data_obj = text_generator.generate_hmm_novel_text(number_of_words_per_sentence , 
                                                          number_of_sentences_per_record , 
                                                          number_of_records)
    elif engine_type == 'simplifiedmarkovchain':
        data_obj = text_generator.generate_simple_markov_chain_novel_text(number_of_words_per_sentence , 
                                                                          number_of_sentences_per_record , 
                                                                          number_of_records)
    elif engine_type == 'cfg':
        data_obj = text_generator.generate_context_free_grammar_novel_text(number_of_words_per_sentence , 
                                                                           number_of_sentences_per_record , 
                                                                           number_of_records)
    if bGenerateUuids:
        data_obj = [(str(uuid.uuid1()) , novel_text) for novel_text in data_obj]
    else:
        data_obj = [(i , novel_text) for i , novel_text in enumerate(data_obj)]
    return data_obj

def main(args):
    fileConfig('config/logging.cfg')
    prop = PropertyUtil('config/app.cfg')
    logger = logging.getLogger(__name__)
    raw_data = ''
    data_obj = [[]]
    try:
        props = _create_property_dict(properties=prop)
        if props['corpora-ref-path-type'] == 'nltk-datafile'and props['corpora-ref-path'].startswith('nltk://'):
            if props['engine-type'] == 'cfg':
                raw_data = _load_nltk_data_as_string(props['corpora-ref-path'], 'nltk://')
            else:
                raw_data = _load_nltk_data(props['corpora-ref-path'], 'nltk://')
        elif props['corpora-ref-path-type'] == 'local-datafile':
            raw_data = _load_local_file(props['corpora-ref-path'])
        elif props['corpora-ref-path-type'] == 'url':
            raw_data = _load_url_data(props['corpora-ref-path'])
        text_gen = TextGenerator(raw_data , logger)
        if props['is-datafile-to-be-generated']:
            data_obj = _generate_array_of_records(text_generator=text_gen, 
                                                  engine_type=props['engine-type'], 
                                                  bGenerateUuids=props['generate-uuids'], 
                                                  corpus=raw_data, 
                                                  number_of_words_per_sentence=props['words-per-sentence'] , 
                                                  number_of_sentences_per_record=props['sentences-per-record'], 
                                                  number_of_records=props['data-file-record-num'])
            if len(data_obj) > 0:
                text_gen.generate_csv(data_obj, 
                                      props['output-file-path'], 
                                      props['datafile-delimiter'])
        if props['is-datafile-to-be-indexed']:
            indexer = SearchEngineIndexer(props['search-engine-url'] , 
                                          props['drop-index-flag'] ,
                                          props['search-index-name'] , 
                                          logger)
            indexer.ingestDataIntoElasticSearchStore(props['output-file-path'], 
                                                     props['datafile-delimiter'], 
                                                     index_model_path='config/index.model.json',
                                                     document_model_path='config/document.model.json', 
                                                     request_model_path='config/search.engine.model.json', 
                                                     refresh=True)
    except IOError , ioerror:
        logger.error('IOError occurred - {0}'.format(str(ioerror)))
        traceback.print_exc()
    except Exception , error:
        logger.error('Error occurred - {0}'.format(str(error)))
        traceback.print_exc()
        
if __name__ == '__main__':
    main(sys.argv)