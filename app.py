from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, NumberRange
from bson import ObjectId
import os

#  the Flask app
app = Flask(__name__)

# ~ MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/movie_reviews"
app.secret_key = os.urandom(24)
mongo = PyMongo(app)

# Movie Review Form
class ReviewForm(FlaskForm):
    movieTitle = StringField('Movie Title', validators=[DataRequired()])
    rating = IntegerField('Rating (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    review = TextAreaField('Review', validators=[DataRequired()])

@app.route('/')
def index():
    # Fetch movies and reviews from MongoDB
    movies = mongo.db.movies.find()
    reviews = mongo.db.reviews.find()
    
    # Convert ObjectId to string for the templates
    reviews = [{**review, "id": str(review["_id"])} for review in reviews]

    return render_template('index.html', movies=movies, reviews=reviews)

@app.route('/api/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        # Return reviews as JSON
        reviews = mongo.db.reviews.find()
        reviews = [{**review, "id": str(review["_id"])} for review in reviews]
        return jsonify(reviews)

    if request.method == 'POST':
        # Add new review to the database
        movie_title = request.json.get('movieTitle')
        rating = request.json.get('rating')
        review = request.json.get('review')

        mongo.db.reviews.insert_one({
            "movieTitle": movie_title,
            "rating": rating,
            "review": review
        })
        return jsonify({"message": "Review added successfully!"}), 201

@app.route('/add_review', methods=['GET', 'POST'])
def add_review():
    form = ReviewForm()

    if form.validate_on_submit():
        # Insert review into the MongoDB database
        mongo.db.reviews.insert_one({
            "movieTitle": form.movieTitle.data,
            "rating": form.rating.data,
            "review": form.review.data
        })
        return redirect(url_for('index'))

    return render_template('add_review.html', form=form)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
