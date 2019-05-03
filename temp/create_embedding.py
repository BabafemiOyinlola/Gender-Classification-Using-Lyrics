import os
from gensim.models.word2vec import Word2Vec

name_of_model = "lyrics_word_embeddings"
feature_size = 200
wind = 8
sample_s = 0.001
workrs = 10
mn_count = 5
skip_gram = 0 #use CBOW

#if model has been trained, use model, else, train word embeddings
def train_word_embeddings(corpus):
    if not os.path.exists(name_of_model): 
        model = Word2Vec(corpus, size=feature_size, window=wind, min_count=mn_count, workers=workrs, sample=sample_s, sg=skip_gram)
        model.save(name_of_model)
        print("Model trained")
    else:
        model = Word2Vec.load(name_of_model)
        print("Returning existing model")
    print("%d songs used in training model" % len(corpus))
    return model


