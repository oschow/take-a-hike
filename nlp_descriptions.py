import pandas as pd
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk import pos_tag
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

if __name__ == '__main__':
    df = pd.read_csv('hike_data_clean.csv')
    df.drop('Unnamed: 0', axis=1, inplace=True)
    descriptions = df['trail_description']

    docs = [word_tokenize(content) for content in descriptions]

    stop = set(stopwords.words('english'))
    docs = [[word for word in words if word not in stop] for words in docs]

    porter = PorterStemmer()
    snowball = SnowballStemmer('english')
    wordnet = WordNetLemmatizer()
    docs_porter = [[porter.stem(word) for word in words] for words in docs]
    docs_snowball = [[snowball.stem(word) for word in words] for words in docs]
    docs_wordnet = [[wordnet.lemmatize(word) for word in words] for words in docs]

    for i in xrange(min(len(docs_porter[0]), len(docs_snowball[0]), len(docs_wordnet[0]))):
        p, s, w = docs_porter[0][i], docs_snowball[0][i], docs_wordnet[0][i]
    if len(set((p, s, w))) != 1:
        print "%s\t%s\t%s\t%s" % (docs[0][i], p, s, w)

    docs = docs_snowball # choose which stemmer/lemmatizer to use
    vocab_set = set()
    [[vocab_set.add(token) for token in tokens] for tokens in docs]
    vocab = list(vocab_set)

    matrix = [[0] * len(vocab) for doc in docs]
    vocab_dict = dict((word, i) for i, word in enumerate(vocab))
    for i, words in enumerate(docs):
        for word in words:
            matrix[i][vocab_dict[word]] += 1

    cv = CountVectorizer(stop_words='english')
    vectorized = cv.fit_transform(descriptions)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidfed = tfidf.fit_transform(descriptions)

    cosine_similarities = linear_kernel(tfidfed, tfidfed)

    for i, doc1 in enumerate(docs):
        for j, doc2 in enumerate(docs):
            print i, j, cosine_similarities[i, j]
