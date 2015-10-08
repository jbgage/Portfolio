'''
@author: bgage
'''
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
    def corpusEngineType(self):
        return self._getstr('Corpus_Parameters' , 'corpus.engine.type')
    
    @property
    def corporaReferencePath(self):
        return self._getstr('Corpus_Parameters' , 'corpora.reference.path')
    
    @property
    def corporaReferencePathType(self):
        return self._getstr('Corpus_Parameters' , 'corpora.reference.path.type')
    
    @property
    def isOperationGenerateDatafile(self):
        return self._getbool('Datafile_Parameters' , 'operation.generate.datafile')
    
    @property
    def dataFileRecordNumber(self):
        return self._getint('Datafile_Parameters' , 'datafile.record.number')
    
    @property
    def sentencesPerRecord(self):
        return self._getint('Datafile_Parameters' , 'datafile.sentences.per.record')
    
    @property
    def wordsPerSentence(self):
        return self._getint('Datafile_Parameters' , 'datafile.words.per.sentence')
    
    @property
    def isGenerateUuids(self):
        return self._getbool('Datafile_Parameters' , 'datafile.generate.uuids')
    
    @property
    def dataFileOutputPath(self):
        return self._getstr('Datafile_Parameters' , 'datafile.output.file.path')
    
    @property
    def dataFileDelimiter(self):
        return self._getstr('Datafile_Parameters' , 'datafile.delimiter')
    
    @property
    def isOperationIndexDataFile(self):
        return self._getbool('Datafile_Parameters' , 'operation.index.datafile')
    
    @property
    def elasticSearchUrl(self):
        return self._getstr('ElasticSearch_Parameters' , 'elastic.search.qualified.url')
    
    @property
    def elasticSearchIndexName(self):
        return self._getstr('ElasticSearch_Parameters' , 'elastic.search.index.name')
    
    @property
    def isDropIndex(self):
        return self._getbool('ElasticSearch_Parameters' , 'drop.index.flag')
    
    