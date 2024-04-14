from flask_restful import Resource, reqparse
from model import db, Rate, Song, roles_required
from sqlalchemy import func
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache import cache

class SubmitRatingResource(Resource):
    @jwt_required()
    def post(self, song_id, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=int, required=True)
        args = parser.parse_args()

        rate_value = args['rating']
        existing_entry = Rate.query.filter_by(userid=user_id, songid=song_id).first()

        if existing_entry:
            existing_entry.ratinggiven = rate_value
            db.session.commit()
        else:
            new_entry = Rate(userid=user_id, songid=song_id, ratinggiven=rate_value)
            db.session.add(new_entry)
            db.session.commit()           

        song = Song.query.get(song_id)
        average_rating = db.session.query(func.avg(Rate.ratinggiven)).filter(Rate.songid == song_id).scalar() or 0
        song.rating = round(average_rating)
        db.session.commit()

        return {'message': 'Rating submitted successfully'}, 200
    
    @jwt_required()
    def get(self, song_id, user_id):
        temp=Rate.query.filter_by(userid=user_id,songid=song_id).first()
        if temp:
            return {'ratevalue':temp.ratinggiven}, 200
        else:
            return {"message":"not rated yet"}, 400
