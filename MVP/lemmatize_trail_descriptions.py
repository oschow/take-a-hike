import numpy as np
import pandas as pd
import re
import pattern.en as en
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer

def stop_words():
    stop = stopwords.words('english') + ['mile', 'miles', 'trail', 'trails', 'north', 'east', 'south', 'west', 'southeast', 'southwest', 'northeast', 'northwest', 'across', 'along', 'easy', 'moderate', 'strenuous', 'colorado', 'aspen', 'snowmass', 'maroon', 'bells', 'boulder', 'eldorado']
    return set(stop)

def lemmatize_descriptions(trail_description):
    '''
    INPUT: trail_description (str) - raw text from the trail descriptions (where text has been lowered and punctuation removed already)
    OUTPUT: lemmatized_text - trail description text with all stopwords removed and the remaining text lemmatized
    '''
    stopwords = stop_words()
    lemmatized_description = ' '.join([en.lemma(w) for w in trail_description.split() if w not in stopwords])
    return ' '.join([w for w in lemmatized_description.split()])

if __name__ == '__main__':
    df = pd.read_csv('data/hike_data_clean.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)

    df['lemmatized_text'] = df['trail_description'].str.replace('Lake','')
    df['lemmatized_text'] = df['lemmatized_text'].apply(lambda x: x.lower())
    df['lemmatized_text'] = df['lemmatized_text'].apply(lambda x: re.sub("[^a-zA-Z]", " ", x))
    df['lemmatized_text'] = df['lemmatized_text'].apply(lemmatize_descriptions)
    descriptions = df['lemmatized_text']

    vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, stop_words = None, max_features = 5000)
    count_vec = vectorizer.fit_transform(descriptions)
    cv = count_vec.toarray()
    vocab = vectorizer.get_feature_names()

    # dist = np.sum(cv, axis=0)
    # # tups = []
    # for tag, count in zip(vocab, dist):
    # #     tup = (count, tag)
    # #     tups.append(tup)
    #     print count, tag
    # # tups.sort()
    # # print tups

    df.to_csv('data/lemmatized_hikes.csv')
