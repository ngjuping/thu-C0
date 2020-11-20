from mongoengine import *
import bson
import bcrypt


class User(DynamicDocument):
    user_id=IntField(required=True)
    name=StringField()
    api_id=StringField(required=True)
    # password hash
    password =BinaryField()
    # password=StringField()
    rent_now=ListField()
    rent_history=ListField()
    invitation=ListField()
    feedback=ListField()
    @classmethod
    def create(cls,  password, **kwargs):
        pw = password.encode('utf-8')
        return cls.objects.create(**kwargs, **{
            'password': bcrypt.hashpw(pw, bcrypt.gensalt())
        })

    def authenticate(self,password):
        pw=password.encode('utf-8')
        return bcrypt.checkpw(pw,self.password)