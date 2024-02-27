#!/usr/bin/python3
"""Places amenities controller"""
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
def get_place_amens(place_id):
    """GET places amenities"""
    place = storage.get('Place', place_id)

    if not place:
        abort(404)

    return jsonify([amenity.to_dict() for amenity in place.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'])
def del_place_amen(place_id, amenity_id):
    """DELETE places amenity"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)

    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'])
def create_place_amenity(place_id, amenity_id):
    """POST places amenity"""
    place = storage.get('Place', place_id)
    if not place:
        abort(404)

    amenity = storage.get('Amenity', amenity_id)
    if not amenity:
        abort(404)

    if amenity not in place.amenities:
        place.amenities.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    else:
        return jsonify(amenity.to_dict()), 200
