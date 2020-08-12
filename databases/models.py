from mongoengine import *
import datetime




class FakeNews(Document):

    #by = ['Public','Machine Learing Model','Official']

    title = StringField(max_length=100,required=True)
    body = StringField(max_length=255,required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    countfake = IntField(default=0)
    countnotfake = IntField(default=0)

    # is_fake = BooleanField(default=None)
    # tags = ListField(StringField(max_length=20))
    #confirmed_by = ListField(StringField(),choices=by)

    def to_json(self):
        return self.to_mongo()

    def isTitleChanged(self,title):
       
        if self.title == title or title == '' or title is None:
          
            return False
        else:
            
            return True

    def isBodyChanged(self,body):
      
         
        if self.body == body or body == '' or body is None:
            
            return False
        else:
           
            return True

    
class User(Document):
    full_name  = StringField(required=True,max_length=50)
    email = EmailField(required=True,unique=True)


class VoteFakeNews(Document):
    #user = ReferenceField(User)
    post = ReferenceField(FakeNews)
    is_fake = BooleanField(default=None)


