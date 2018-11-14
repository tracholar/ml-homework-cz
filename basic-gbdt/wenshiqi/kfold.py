# coding=utf-8

import numpy as np


class Kfold(object):

    def __init__(self, n_splits=3, shuffle=False,
                 random_state=None):
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state


    def _iter_test_indices(self, X, y=None):
        n_samples = len(X)
        indices = np.arange(n_samples)
        if self.shuffle:
            np.random.seed(self.random_state)
            np.random.shuffle(indices)

        n_splits = self.n_splits
        fold_sizes = (n_samples // n_splits) * np.ones(n_splits, dtype=np.int)
        fold_sizes[:n_samples % n_splits] += 1
        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            yield indices[start:stop]
            current = stop

    def split(self, X, y=None):

        indices = np.arange(len(X))
        for test_index in self._iter_test_indices(X, y):
            train_index = indices[np.logical_not(test_index)]
            test_index = indices[test_index]
            yield train_index, test_index