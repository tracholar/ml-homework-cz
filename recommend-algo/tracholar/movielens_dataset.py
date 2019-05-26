#coding:utf-8

import os
import pandas as pd

class Movie():
    def __init__(self, movieId,title,genres):
        self.movieId = movieId
        self.title = title
        self.genres = genres
    def __repr__(self):
        return '<MOVIE {}:{}>'.format(self.movieId, self.title)


class MovieLens(object):
    def __init__(self, debug = False):
        root = os.path.abspath('.')
        if not os.path.exists(root + '/ml-20m'):
            os.system('sh download_dataset.sh')
        self.root = root + '/ml-20m/'
        self.debug = debug

    user_like_list = None
    def get_user_like_list(self):
        if self.user_like_list is not None:
            return self.user_like_list
        if self.debug:
            df = pd.read_csv(self.root + 'ratings.csv', nrows=10000)
        else:
            df = pd.read_csv(self.root + 'ratings.csv')
        df = df[df.rating >= 4].groupby('userId')\
            .apply(lambda x: x.movieId.tolist())  # 认为4分以上是喜欢的电影
        self.user_like_list = df
        return self.user_like_list

    movies = None


    def get_movie_list(self, idlist):
        if self.movies is None:
            self.movies = dict()
            df = pd.read_csv(self.root + 'movies.csv')
            for _, row in df.iterrows():
                self.movies[row['movieId']] = Movie(**row)

        return [self.movies[i] for i in idlist]

if __name__ == '__main__':
    dataset = MovieLens()
    print dataset.get_user_like_list()