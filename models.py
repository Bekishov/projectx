from peewee import * 
import datetime 
from  flask_login import UserMixin

db = PostgresqlDatabase(
    'flask_db',
    host = 'localhost',
    port = 5432,
    user = 'flask_user',
    password = 'qwe123'
)
class BaseModel(Model):
    class Meta:
        database = db
    


class MyUser(BaseModel, UserMixin):
    email = CharField(max_length=225, null = False, unique = True)
    name = CharField(max_length=225, null = False)
    second_name = CharField(max_length=225, null = False)
    password = CharField(max_length=225, null = False)
    age = IntegerField()

    def repr(self):
        return self.email

    
class Post(BaseModel):
    author = ForeignKeyField(MyUser, on_delete='CASCADE')
    title = CharField(max_length=225, null = False)
    description = TextField()
    date = DateTimeField(default=datetime.datetime.now)


    def repr(self):
        return self.title
    

    
db.create_tables([Post,MyUser])

