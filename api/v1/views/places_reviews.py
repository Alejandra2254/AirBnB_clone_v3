#!/usr/bin/python3
"""View configuration for Places-Review"""
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage, place
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """Gets all reviwes depending of place_id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    res = []
    for i in city.reviews:
        res.append(i.to_dict())
    return jsonify(res)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id=None):
    """Gets a review according with the id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id=None):
    """Deletes a review according with the id"""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    review.delete()
    storage.save()
    return (jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_placereview(place_id):
    """Create a review"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    content_review = request.get_json()
    if content_review is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    elif 'user_id' not in content_review:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user_info = storage.get("User", content_review['user_id'])
    if user_info is None:
        abort(404)
    if 'text' not in content_review:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    content["place_id"] = place_id
    new_s = Review(**content_review)
    new_s.save()
    return make_response(jsonify(new_s.to_dict()), 201)


@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def put_placereview(review_id):
    """Updates a user with a given id"""
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    content = request.get_json()
    review = storage.get('Review', review_id)
    if review is None:
        abort(404)
    if not content:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, val in content.items():
        if key not in ignore_keys:
            setattr(review, key, val)
    storage.save()
    return (jsonify(review.to_dict()), 200)
