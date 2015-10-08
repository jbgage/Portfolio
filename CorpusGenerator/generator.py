'''
Created on Sep 26, 2015

@author: bgage
'''
import nltk
import random
import csv
import os
import re
import sys
import string
import itertools
from nltk.util import ngrams
from nltk import word_tokenize 
from nltk.grammar import CFG
from nltk.grammar import PCFG
from nltk.parse.chart import ChartParser 
from nltk.grammar import FeatureGrammar 
from nltk.parse.featurechart import FeatureChartParser
from nltk.parse.pchart import InsideChartParser
from nltk.parse.generate import generate as generate_text
from nltk.grammar import Nonterminal

class TextGenerator(object):
    

    def __init__(self, corpus_text_input='' , logger=None):
        self._corpus = corpus_text_input
        self.logger = logger
    
    def generate_simple_markov_chain_novel_text(self , number_of_words_in_sentence=0 , number_of_sentences_per_record=0 , number_of_records=0 ):
        tokens = word_tokenize(self._corpus)
        cache = {}
        words = []
        try:
            bigrams = ngrams(tokens , 2)
            for word1 , word2 in bigrams:
                key = (word1)
                if key in cache:
                    cache[key].append(word2)
                else:
                    cache[key] = [word2]
            word_size = len(tokens)
            seed = random.randint(0 , word_size-2)
            seed_word , next_word = tokens[seed] , tokens[seed + 1]
            word1 , word2 = seed_word , next_word
            for _ in range(number_of_records):
                for _ in range(number_of_sentences_per_record):
                    for _ in range(number_of_words_in_sentence):
                        words.append(word1)
                        word1 , word2 = word2 , random.choice(cache[(word1)])
                    words.append(word2)
                [item.replace('. .' , '.')  for item in words]
        except Exception , error:
            self.logger.error('TextGenerator.generate_simple_markov_chain_novel_text: Error occurred - {0}'.format(str(error)))
        return words
    
    def _tag_and_parse_corpus(self , corpus=''):
        tag_re = re.compile(r'[*]|--|[^+*-]+')
        tag_set = set()
        symbols = set()
        cleaned_sentences = []
        try:
            sent_tokens = nltk.sent_tokenize(corpus)
            word_tokens = [nltk.word_tokenize(sentence.replace('\'' , '')) for sentence in sent_tokens]
            tagged_tokens = [nltk.pos_tag(tokens) for tokens in word_tokens]
            for sequence in tagged_tokens:
                for i in range(len(sequence)):
                    word , tag = sequence[i]
                    symbols.add(word)
                    tag = tag_re.match(tag).group()
                    tag_set.add(tag)
                    sequence[i] = (word , tag)
                cleaned_sentences.append(sequence) 
        except Exception , error:
            self.logger.error('TextGenerator._tag_and_parse_corpus: Error occurred - {0}'.format(str(error)))
        return cleaned_sentences , list(tag_set) , list(symbols)
    
    def generate_hmm_novel_text(self ,  number_of_words_in_sentence=0 , number_of_sentences_per_record=0 , number_of_records=0 ):
        words = []
        punct_selector = ['. ' , '! ' , '? ']
        punctuation_stop_symbols = dict((ord(char) , None) for char in string.punctuation)
        try:
            labelled_sequence , tag_set , symbols = self._tag_and_parse_corpus(self._corpus)
            trainer = nltk.tag.hmm.HiddenMarkovModelTrainer(tag_set , symbols)
            hmm = trainer.train_supervised(labelled_sequence , estimator=lambda fd , bins: nltk.probability.LidstoneProbDist(fd , 0.1 , bins))
            rng = random.Random(len(self._corpus))
            for _ in range(number_of_records):
                novel_sentence = []
                for _ in range(number_of_sentences_per_record):
                    sentence = ' '.join(word[0] for word in hmm.random_sample(rng , number_of_words_in_sentence ))
                    sentence = sentence.translate(punctuation_stop_symbols) + random.choice(punct_selector)
                    sentence = sentence[0:].capitalize()
                    novel_sentence.append(sentence)
                words.append(''.join(novel_sentence))
        except Exception , error:
            self.logger.error('TextGenerator.generate_hmm_novel_text: Error occurred - {0}'.format(str(error)))   
        return words
     
        
    def generate_context_free_grammar_novel_text(self , number_of_words_in_sentence=0 , number_of_sentences_per_record=0,  number_of_records=0):
        words = []
        punct_selector = ['. ' , '! ' , '? ']
        punctuation_stop_symbols = dict((ord(char) , None) for char in string.punctuation)
        parser = None
        grammar = None
        try:
            if isinstance(self._corpus , CFG):
                _grammar = self._corpus
                if _grammar is not None:
                    parser = ChartParser(_grammar)
                    grammar = parser.grammar
            elif isinstance(self._corpus , FeatureGrammar):
                _grammar = self._corpus
                if _grammar is not None:
                    parser = FeatureChartParser(_grammar)
                    grammar = parser.grammar()
            elif isinstance(self._corpus , PCFG):
                _grammar = self._corpus
                if _grammar is not None:
                    parser = InsideChartParser(_grammar)
                    grammar = parser.grammar()
            else:
                grammar = CFG.fromstring(self._corpus)
            if grammar is not None:        
                for _ in range(number_of_records):
                    novel_sentence = []
                    for _ in range(number_of_sentences_per_record):
                        sentence = ' '.join([sent for _ , sent in enumerate(generate_text(grammar , depth=2 , n=number_of_words_in_sentence))])
                        sentence = sentence.translate(punctuation_stop_symbols) + random.choice(punct_selector)
                        sentence = sentence[0:].capitalize()
                        novel_sentence.append(sentence)
                    words.append(''.join(novel_sentence))
        except Exception , error:
            self.logger.error('TextGenerator.generate_context_free_grammar_novel_text: Error occurred - {0}'.format(str(error)))   
        return '. '.join(words)
    
    def generate_direct_text(self , number_of_sentences=0 , number_of_records=0):
        words=[]
        sentence_tokens = nltk.sent_tokenize(self._corpus)
        words = [random.choice(sentence_tokens) for _ in range(number_of_sentences) for _ in range(number_of_records)]
        return words
        
    
    def generate_csv(self , data=[] , output_file_name='' , delimiter=''):
        try:
            if len(data) > 0:
                abs_path = os.path.abspath(output_file_name)
                with open(abs_path , 'wb') as csv_file:
                    csv_writer = csv.writer(csv_file , delimiter=delimiter)
                    csv_writer.writerows(data)
            else:
                self.logger.error('There was an error retrieving the data as an array. Its length was zero.')
        except IOError , ioerror:
            self.logger.error('TextGenerator.generate_csv: IOError occurred - {0}'.format(str(ioerror)))   
        except Exception , error:
            self.logger.error('TextGenerator.generate_csv: Error occurred - {0}'.format(str(error)))   
            
            