'''
@author: jbgage
'''
import numpy as np
import string
import nltk
import phrase
import vector
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords

class LingoClustering(object):
    
    _COMMON_WORD = 0
    _UNCOMMON_WORD = 1

    def __init__(self, logger=None , corpus=[] , stop_words = stopwords.words('English') ):
        self._logger = logger
        self._query = ''
        self._documents = corpus
        self._clusters = []
        self._scoreWeight = 0.0
        self._stoplist = stop_words
        
    def __preprocess(self):
        stemmer = PorterStemmer()
        punctuation_stop_symbols = dict((ord(char) , None) for char in string.punctuation)
        stemmed_corpus = []
        labeled_corpus = []
        try:
            sent_tokens = nltk.sent_tokenize(self._documents)
            word_tokens = [nltk.word_tokenize(sentence.translate(punctuation_stop_symbols)) for sentence in sent_tokens]
            stemmed_corpus = [stemmer.stem(word.lower()) for word in word_tokens]
            for word in stemmed_corpus:
                if word in self._stoplist:
                    labeled_corpus.append((word , self._COMMON_WORD))
                else:
                    labeled_corpus.append((word , self._UNCOMMON_WORD))
        except Exception , error:
            self._logger.error("LingoClustering._preprocess: Error occurred - {0}" , str(error))
        return labeled_corpus
    
    def __phrase_frequency_extraction(self , corpus = [] , term_frequency_threshold=4):
        frequency_dist = []
        try:
            chunker = phrase.PhraseChunker(corpus)
            chunked_sentences = [chunker.parser(sentence) for sentence in corpus]
            raw_frequency_dist = nltk.FreqDist(' '.join(chunked_sentences))
            for (term , freq) in enumerate(raw_frequency_dist):
                if freq < term_frequency_threshold:
                    frequency_dist.append((term , freq))
        except Exception , error:
            self._logger.error("LingoClustering.__phrase_frequency_extraction: Error occurred - {0}" , str(error))
        return frequency_dist
    
    def __term_frequency_extraction(self , corpus=[] , term_frequency_threshold=4 ):
        frequency_dist =[]
        try:
            raw_frequency_dist = nltk.FreqDist(' '.join(corpus))
            for (term , freq) in enumerate(raw_frequency_dist):
                if freq < term_frequency_threshold:
                    frequency_dist.append((term , freq))
        except Exception , error:
            self._logger.error("LingoClustering.__term_frequency_extraction: Error occurred - {0}" , str(error))
    
    def cluster_label_induction(self):
        clusters = []
        vectorizer = vector.StemmedVectorizer()
        try:
            term_matrix = self.__term_frequency_extraction(self._documents)
            Ut , st , Vt = np.linalg.svd([term[1] for term in term_matrix])
            term_rank = np.linalg.matrix_rank(term_matrix)
            phrase_freqs = self.__phrase_frequency_extraction(self._documents)
            phrase_cluster = [phrase_freq[0] for phrase_freq in phrase_freqs ]
            phrase_matrix = vectorizer.fit_transform(' '.join(phrase_cluster)).toarray()
            for i , phrase in enumerate(phrase_matrix):
                label_score = phrase.index(max(phrase))
                clusters.append((phrase_matrix.get_feature_names[i] , label_score))                         
        except Exception , error:
            self._logger.error("LingoClustering.__term_frequency_extraction: Error occurred - {0}" , str(error))
        return clusters  
        