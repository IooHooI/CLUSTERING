from sklearn.base import BaseEstimator, TransformerMixin
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from tqdm import tqdm
import numpy as np


class Doc2VecTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, size=300, alpha=0.025, window=8, min_count=5, sample=1e-3, negative=5, epochs=20):
        self.size = size
        self.alpha = alpha
        self.window = window
        self.min_count = min_count
        self.sample = sample
        self.negative = negative
        self.epochs = epochs
        self._model = None

    def fit(self, X, y=None):
        tagged_data = [TaggedDocument(words=_d, tags=[str(i)]) for i, _d in enumerate(list(map(str.split, X)))]
        self._model = Doc2Vec(vector_size=self.size, alpha=self.alpha, min_alpha=0.00025, min_count=self.min_count, dm=1)
        self._model.build_vocab(tagged_data)
        for _ in tqdm(self.epochs):
            self._model.train(tagged_data, total_examples=self._model.corpus_count, epochs=self._model.iter)
            # decrease the learning rate
            self._model.alpha -= 0.0002
            # fix the learning rate, no decay
            self._model.min_alpha = self._model.alpha
        self._model = self._model
        return self

    def fit_transform(self, X, y=None, **fit_params):
        self.fit(X, y)
        return self._model.docvecs

    def transform(self, X, copy=True):
        assert self._model is not None, 'model is not fitted'
        return np.asmatrix(np.array([self._model.infer_vector(document.words) for document in X]))
