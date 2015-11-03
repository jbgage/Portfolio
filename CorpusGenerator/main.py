#!/usr/bin/env python
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

def __load_nltk_data(file_path='' , prefix='' ):
    '''
    This method loads the NLTK corpus as an object. The path is prepended by the prefix 'nltk://' 
    to denote the fact that this corpus is from the NLTK's corpora of data.
    
    @param file_path: The path to the NTLK file reference
    @type file_path: str 
    @param prefix: The prefix used to denote whether the corpus is part of the NLTK corpora
    @type prefix: str
    @return: object
    '''
    return nltk.data.load(file_path[len(prefix):] )

def __load_nltk_data_as_string(file_path='' , prefix='' ):
    '''
    This method is similar to the one above it except this method returns the corpus as a string rather than an object.
    
    @param file_path: The path to the NTLK file reference
    @type file_path: str 
    @param prefix: The prefix used to denote whether the corpus is part of the NLTK corpora
    @type prefix: str
    @return: str
    '''
    return nltk.data.load(file_path[len(prefix):] , format='text' )

def __load_url_data(url=''):
    '''
    This method loads data from a specified URL
    
    @param url: URL that contains the data which will be used
    @type url: str
    @return: str
    '''
    response = urllib2.urlopen(url)
    return response.read()

def __load_local_file(file_path='' ):
    '''
    This method loads the file specified from the source file system.
    
    @param file_path: The relative or absolute path of the data file contained on the source file system.
    @type file_path: str
    @return: str
    '''
    data = ''
    if os.path.isfile(file_path):
        with open(file_path) as local_file:
            data = local_file.read()
    return data

def __create_property_dict(properties=None):
    '''
    This method loads the property file getters from the PropertyUtil object parameter
    
    @param properties: The PropertyUtil object that contains the property files from app.cfg
    @type properties: property.PropertyUtil
    @return: dict
    '''
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

def __generate_array_of_records(text_generator=None , 
                               engine_type='' , 
                               bGenerateUuids=True , 
                               corpus='' , 
                               number_of_words_per_sentence=0 , 
                               number_of_sentences_per_record=0 , 
                               number_of_records=0):
    '''
    This method is a utility method that is charged with invoking the different novel text generators above (based upon various 'engines'
    contained in config/app.cfg).
    
    @param text_generator: The text generator object.
    @type text_generator: generator.TextGenerator
    @param engine_type: The engine type referenced in config/app.cfg.
    @type engine_type: str
    @param bGenerateUuids: Parameter that indicates whether GUIDs are to be created per record
    @type bGenerateUuids: bool
    @param corpus: This is the training corpus
    @type corpus: str
    @param number_of_words_in_sentence: An indicator as to the number of words to generate in each novel sentence.
    @type number_of_words_per_sentence: int
    @param number_of_sentences_per_record: An indicator as to the number of sentences per record to generate.
    @type number_of_sentences_per_record: int
    @param number_of_records: An indicator as to the total number of records to generate.
    @type number_of_records: int
    @return: list
    '''
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
        props = __create_property_dict(properties=prop)
        if props['corpora-ref-path-type'] == 'nltk-datafile'and props['corpora-ref-path'].startswith('nltk://'):
            if props['engine-type'] == 'cfg':
                logger.info('Loading Chomsky-normalized Context Free Grammars...')
                raw_data = __load_nltk_data_as_string(props['corpora-ref-path'], 'nltk://')
            else:
                logger.info('Loading data directly from the NLTK corpora stored on the file system...')
                raw_data = __load_nltk_data(props['corpora-ref-path'], 'nltk://')
        elif props['corpora-ref-path-type'] == 'local-datafile':
            logger.info('Loading data directly from the file system...')
            raw_data = __load_local_file(props['corpora-ref-path'])
        elif props['corpora-ref-path-type'] == 'url':
            logger.info('Loading data from URLs...')
            raw_data = __load_url_data(props['corpora-ref-path'])
        text_gen = TextGenerator(raw_data , logger)
        if props['is-datafile-to-be-generated']:
            logger.info('Data-file will be generated utilizing the selected engine type: {0}..'.format(props['engine-type']))
            data_obj = __generate_array_of_records(text_generator=text_gen, 
                                                  engine_type=props['engine-type'], 
                                                  bGenerateUuids=props['generate-uuids'], 
                                                  corpus=raw_data, 
                                                  number_of_words_per_sentence=props['words-per-sentence'] , 
                                                  number_of_sentences_per_record=props['sentences-per-record'], 
                                                  number_of_records=props['data-file-record-num'])
            if len(data_obj) > 0:
                logger.info('Generating CSV files...')
                text_gen.generate_csv(data_obj, 
                                      props['output-file-path'], 
                                      props['datafile-delimiter'])
        if props['is-datafile-to-be-indexed']:
            logger.info('Datafile with be indexed...')
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