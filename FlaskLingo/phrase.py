'''
Created on Oct 28, 2015

@author: jbgage
'''
import nltk
class PhraseTagger(nltk.TaggerI):
    
    def __init__(self, training_sentences):
        training_set = []
        for sent in training_sentences:
            untagged_sentence = nltk.tag.untag(sent)
            history = []
            for i , (word , pos_tag) in enumerate(sent):
                features = self.__chunk_features(untagged_sentence , i , history)
                training_set.append((features , pos_tag))
                history.append(pos_tag)
        self.classifier = nltk.MaxentClassifier.train(training_sentences , algorithm='megam' , trace=0)
    
    def __chunk_features(self , sentence=[] , i , history):
        word , pos = sentence[i]
        return {'pos':pos}

    def tag(self , sentence=[]):
        history =[]
        for i , word in enumerate(sentence):
            features = self.__chunk_features(sentence, i, history)
            tag = self.classifier.classify(features)
            history.append(tag)
        return zip(sentence , history)
    
class PhraseChunker(nltk.ChunkParserI):
    def __init__(self , training_sentences=[]):
        tagged_sentences = [[((word , tag ) , iob) for (word , tag , iob) in nltk.chunk.tree2conlltags(sentence)] for sentence in training_sentences]
        self.tagger = PhraseTagger(tagged_sentences)
    
    def parse(self , sentence):
        tagged_sentence = self.tagger.tag(sentence)
        tags = [(word , tag , iob) for ((word , tag) , iob) in tagged_sentence ]
        return nltk.chunk.conlltags2tree(tags)