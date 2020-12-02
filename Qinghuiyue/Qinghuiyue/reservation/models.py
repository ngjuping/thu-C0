from mongoengine import *
import bson
import bcrypt
class Queue_reservation(DynamicDocument):
    reservation_id = IntField()
    user_id = IntField()
    sport_type = IntField()
    day = StringField()
    time_from = StringField()
    time_to = StringField()
    status = StringField()
    type = IntField()  # 抽签方式？


class Reservation(DynamicDocument):
    type = IntField()
    details = DictField()
    status = IntField()
    reservation_id = IntField()

    @classmethod
    def get_reservation_info(cls, objectID):
        rent = cls.objects(id=objectID).first()
        if rent:
            return {
                "reservation_id": rent.reservation_id,
                "type": rent.type,
                "status": rent.status,
                "details": {
                    "name": Court.objects(id=rent.details['court'])[0].name,
                    "start": rent.details['start'],
                    "end": rent.details['end']
                }
            }