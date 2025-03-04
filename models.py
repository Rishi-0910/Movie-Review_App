from flask_pymongo import PyMongo

class Review:
    def __init__(self, movieTitle, rating, review):
        self.movieTitle = movieTitle
        self.rating = rating
        self.review = review
