'''
Created on Oct 12, 2015

@author: jbgage
'''
from gensim import models
from gensim import similarities
from gensim import corpora
import json

class TopicAnalyzer(object):
    
    def __init__(self, corpusText=[] , logger=None):
        self._corpusText = ''.join(corpusText)
        self._corpus = corpusText
        self._stoplist = set('for a of the and to in'.split())
        self._texts = [[word for word in document.lower().split() if word not in self._stoplist]
         for document in self._corpus]
        self._all_tokens = sum(self._texts , [])
        self._tokens_once = set(word for word in set(self._all_tokens) if self._all_tokens.count(word) == 1)
        self._tokenized_text = [[word for word in text if word not in self._tokens_once] for text in self._texts]
        self._logger = logger
        
    def getBowTransformation(self):
        raw_corpus = []
        try:
            dictionary = corpora.dictionary(self._corpus)
            raw_corpus = [dictionary.doc2bow(t) for t in self._corpus] 
        except Exception , error:
            self._logger.error('TopicAnalyzer.getBowTransformation: Error occurred - {0}'.format(str(error)))
        return raw_corpus
        
    def getTfiIdfModel(self):
        tfidfModel = None
        try:
            raw_corpus = self.getBowTransformation()
            tfidfModel = models.TfidfModel(raw_corpus)
        except Exception , error:
            self._logger.error('TopicAnalyzer.getTfIdfModel: Error occurred - {0}'.format(str(error)))
        return tfidfModel
    
    def getTfIdf(self):
        sims = None
        try:
            tfidf = self.getTfiIdfModel()
            if tfidf is not None:
                raw_corpus = self.getBowTransformation()
                corpus_tfidf = tfidf[raw_corpus]
                index = similarities.MatrixSimilarity(tfidf[raw_corpus])
                sims = index[corpus_tfidf]
        except Exception , error:
            self._logger.error('TopicAnalyzer.getTfIdf(): Error occurred - {0}'.format(str(error)))
        return json.dumps((list(enumerate(sims))))
    
    def getLSI(self):
        corpus_tfidf = self.getTfIdfModel()
        dictionary = corpora.Dictionary(self._tokenized_text)
        lsi = models.LsiModel(corpus_tfidf , dictionary=dictionary ,  num_topics=2)
        corpus_lsi = lsi[corpus_tfidf]
        return json.dumps(corpus_lsi)
    
    def getLDA(self):
        dictionary = corpora.Dictionary(self._tokenized_text)
        normalized_corpus = [dictionary.doc2bow(t) for t in self._texts]
        lda = models.ldamodel.LdaModel(normalized_corpus , num_topics=4)
        return json.dumps(lda.show_topic(num_topics=4, formatted=True, topn=20))
        
    
        