'''
Created on Oct 12, 2015

@author: jbgage
'''
from gensim import models
from gensim import similarities
from gensim import corpora
from collections import defaultdict
import json

class TopicAnalyzer(object):
    
    def __init__(self, corpusText=[] , logger=None):
        self._corpus = corpusText
        self._stoplist = set('for a of the and to in'.split())
        self._logger = logger
        
    def _tokenize_words_in_corpus(self):
        return [[word for word in document.lower().split() if word not in self._stoplist] for document in self._corpus ]
    
    def _get_word_frequency_from_tokenized_corpus(self , tokenized_corpus = [[]]):
        freq = defaultdict(int)
        for text in tokenized_corpus:
            for token in text:
                freq[token] += 1
        return freq
    
    def _transform_corpus_by_word_freq(self , tokenized_corpus=[[]] , frequency_dict = {}, word_frequency_floor=1):
        text = [[token for token in text if frequency_dict[token] > word_frequency_floor] for text in tokenized_corpus]
        return text
    
    def _get_corpora_dictionary_from_transformed_corpus(self , corpus=[[]]):
        return corpora.Dictionary(corpus)
    
    def _get_bag_of_words_count_from_dictionary(self , dictionary={} , corpus=[[]]):
        return [dictionary.doc2bow(text) for text in corpus]
    
    def _get_tfidf_from_bow(self , bow_corpus=[]):
        tfidf = models.TfidfModel(bow_corpus)
        return tfidf  
    
    
    
    def _get_transformed_corpus(self , frequency_floor=1):
        tokenized_corpus = self._tokenize_words_in_corpus()
        word_freq = self._get_word_frequency_from_tokenized_corpus(tokenized_corpus)
        transformed_corpus = self._transform_corpus_by_word_freq(tokenized_corpus, word_freq, frequency_floor)
        return transformed_corpus
    
    def _json_transform(self , model=None , bag_of_words=None):
        _json_array = []
        if model is not None and bag_of_words is not None:
            for record in model[bag_of_words]:
                for elem in record:
                    json_elem = {}
                    json_elem['id'] = elem[0]
                    json_elem['value'] = elem[1]
                    _json_array.append(json_elem)
        return json.dumps(_json_array)
    
    def get_tfidf(self , frequency_floor=1):
        tfidf = None
        transformed_corpus = [[]]
        try:
            transformed_corpus = self._get_transformed_corpus(frequency_floor)
            dictionary = self._get_corpora_dictionary_from_transformed_corpus(transformed_corpus)
            bow = self._get_bag_of_words_count_from_dictionary(dictionary, transformed_corpus)
            tfidf = models.TfidfModel(bow , id2word=dictionary)
        except Exception , error:
            self._logger.error("TopicAnalyzer.get_tfidf: Error occurred - {0}".format(str(error)))
        return tfidf , bow
    
    def get_tfidf_as_json(self , frequency_floor=1):
        json_data = {}
        (tfidf , bow) = self.get_tfidf(frequency_floor)
        json_data = self._json_transform(model=tfidf , bag_of_words=bow)
        return json_data
    
    def get_lsi(self , frequency_floor=1 , number_of_topics=5):
        lsi = None
        transformed_corpus = [[]]
        try:
            (corpus_tfidf , bow )= self.get_tfidf(frequency_floor)
            if corpus_tfidf is not None:
                transormed_corpus = self._get_transformed_corpus(frequency_floor)
                dictionary = self._get_corpora_dictionary_from_transformed_corpus(transormed_corpus)
                lsi = models.LsiModel(corpus_tfidf[bow] , id2word = dictionary , num_topics=number_of_topics)
            else:
                self._logger.error("Error occurred. TFIDF was irretrievable.")
        except Exception , error:
            self._logger.error("TopicAnalyzer.get_lsi: Error occurred - {0}".format( str(error)))
        return self._json_transform(lsi , bow)
    
    def get_lda(self , frequency_floor=1 , num_topics=5 , sample_ratio=5):
        ldaModel = None
        corpus = [[]]
        try:
            corpus = self._get_transformed_corpus(frequency_floor)
            if corpus is not None and len(corpus) > 0:
                corpus_dictionary = self._get_corpora_dictionary_from_transformed_corpus(corpus)
                bow = self._get_bag_of_words_count_from_dictionary(corpus_dictionary, corpus)
                ldaModel = models.LdaModel(bow , id2word=corpus_dictionary , num_topics=num_topics , alpha='auto' , eval_every=sample_ratio)
        except Exception , error:
            self._logger.error("TopicAnalyzer.get_lda: Error occurred - {0}".format(str(error)))
        return self._json_transform(ldaModel , bow)
    
    
    