# Goksel Tokur - 150116049 Merve Ayer 150119828 Zahide Tastan 150119827 Ertugrul Sagdic 150116061
import os
import random
import sys
import jpype
import pandas as pd
import numpy as np
import sklearn
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

import codecs
from jpype import JClass, JString, getDefaultJVMPath, shutdownJVM, startJVM
from word import Word
import glob
from nltk.probability import ConditionalFreqDist
from nltk.tokenize import RegexpTokenizer, sent_tokenize

# word - sum of letter values equal to a given number.
word_sum = 100
number_of_words = 5
# sentence - sum of letter values equal to a given number.
sentence_sum = 300
path = "1150haber"
wordLimit = 100000


def init_jvm(jvmpath=None):
    if jpype.isJVMStarted():
        return
    jpype.startJVM(jpype.getDefaultJVMPath(), '-Djava.class.path=zemberek/zemberek-full.jar', "-ea")



init_jvm()
turkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
analysisFormatters = JClass('zemberek.morphology.analysis.AnalysisFormatters')
WordAnalysis = JClass('zemberek.morphology.analysis.WordAnalysis')
morphology = turkishMorphology.createWithDefaults()


fileNames = [subdir + os.path.sep + file for subdir, dirs, files in os.walk(path) for file in files]
# fileNames = [fileName.replace('\\','/') for fileName in fileNames ] # you may add this line for windows os

tfidfVectorizer = TfidfVectorizer(decode_error='ignore')
docTermMatrix = tfidfVectorizer.fit_transform((open(f, encoding="ISO-8859-1").read() for f in fileNames))
word_obj = Word('name', 'type')
word_list = [word[0] for i, word in zip(range(0, wordLimit), tfidfVectorizer.vocabulary_.items())]

noun_list = []
verb_list = []
adj_list = []


# Fill the noun, verb, adj list
def filter_type():
    for word in word_list:
        results = morphology.analyze(word)
        for result in results:
            print(result.getStems(), result.getMorphemes())
            if result.getMorphemes()[0].toString() == "Noun:Noun":
                noun_list.append(Word(result.getStems()[0], 'noun'))
                break
            if result.getMorphemes()[0].toString() == "Verb:Verb":
                verb_list.append(Word(result.getStems()[0], 'verb'))
                break
            if result.getMorphemes()[0].toString() == "Adjective:Adj":
                adj_list.append(Word(result.getStems()[0], 'adj'))
                break

def generate_word():
    i = number_of_words
    while True:
        for word in word_list:
            total = 0
            cont  = True
            values = []
            for letter in word:
                if letter not in word_obj.letterValue:
                    cont = False
                    continue
                values.append(word_obj.letterValue[letter])
                total = total + word_obj.letterValue[letter]
            if cont == False:
                continue
            if i == 0:
                break
            if total == word_sum:
                i = i - 1
                print(word, total)
            
        if i == 0:
            break



# Generate sentence
def generate_sentence():
    while True:
        try:
            noun_word = noun_list[random.randrange(len(noun_list))]
            verb_word = verb_list[random.randrange(len(verb_list))]
            adj_word = ''

            remain = sentence_sum - noun_word.value - verb_word.value
            for adj in adj_list:
                if adj.value == remain:
                    adj_word = adj
                    break
            return f' {adj_word.name} {noun_word.name} {verb_word.name}'
            break
        except AttributeError:
            continue



def main():
    filter_type()

    sum_filtered_words = []
    for word in noun_list:
        if word.value == word_sum:
            sum_filtered_words.append(word)
    for word in verb_list:
        if word.value == word_sum:
            sum_filtered_words.append(word)
    for word in adj_list:
        if word.value == word_sum:
            sum_filtered_words.append(word)

    sum_filtered_words = set(sum_filtered_words)  # to unique it
    #print(sum_filtered_words)

    print('\n\n================GENERATED WORDS====================\n\n')
    print(generate_word())
    print('\n\n================GENERATED SENTENCE====================\n\n')
    print(generate_sentence())
    print('\n\n======================================================')



if __name__ == '__main__':
    main()