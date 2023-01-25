from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import Booking
from model.users import User

booking_api = Blueprint('booking_api', __name__,
                   url_prefix='/api/bookings')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(booking_api)

class BookingAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            name = body.get('name')
            if name is None or len(name) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            
            uid = body.get('uid')
            if uid is None or len(uid) < 2:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            
            bookingid = body.get('bookingid')
            if bookingid is None or len(bookingid) < 2:
                return {'message': f'Booking ID is missing, or is less than 2 characters'}, 210
            ''' #1: Key code block, setup USER OBJECT '''
            booking = Booking(bookingid, name, 
                      uid)
                        
            ''' #2: Key Code block to add booking to database '''
            # create booking in database
            new_booking = booking.create()
            # success returns json of user
            if new_booking:
                return jsonify(new_booking.read())
            # failure returns error
            return {'message': f'Processed {name}, either a format error or User ID {uid} is duplicate'}, 210

    class _Read(Resource):
        def get(self):
            bookings = Booking.query.all()    # read/extract all bookings from database
            json_ready = [booking.read() for booking in bookings]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')