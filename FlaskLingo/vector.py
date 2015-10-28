'''
Created on Oct 28, 2015

@author: jbgage
'''
from sklearn.feature_extraction.text import CountVectorizer
class StemmedVectorizer(CountVectorizer):
    def build_analyzer(self , documents=[]):
        analyzer = super(StemmedVectorizer , self).build_analyzer()
        return lambda phrases: (phrase for phrase in analyzer(phrases))
        