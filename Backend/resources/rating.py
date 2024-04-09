from flask_restful import Resource, reqparse
from model import db, Rate, Song
from sqlalchemy import func

class SubmitRatingResource(Resource):
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

        # song = Song.query.get(song_id)
        # all_ratings = Rate.query.filter_by(songid=song_id).all()
        # count = len(all_ratings)
        # total_rating = sum(int(rate.ratinggiven) for rate in all_ratings)
        # average_rating = total_rating / count if count > 0 else 0
        # song.rating = round(average_rating)
        # db.session.commit()
            

        song = Song.query.get(song_id)
        average_rating = db.session.query(func.avg(Rate.ratinggiven)).filter(Rate.songid == song_id).scalar() or 0
        song.rating = round(average_rating)
        db.session.commit()

        return {'message': 'Rating submitted successfully'}, 200
    
    def get(self, song_id, user_id):
        # if user_id==0:
        #     return {"message":"no user"}, 400
        temp=Rate.query.filter_by(userid=user_id,songid=song_id).first()
        if temp:
            return {'ratevalue':temp.ratinggiven}, 200
        else:
            return {"message":"not rated yet"}, 400
