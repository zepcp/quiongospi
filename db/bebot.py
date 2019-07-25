import settings

import peewee
import time

from playhouse.postgres_ext import ArrayField
from strings import bebot as strings

db = peewee.PostgresqlDatabase(settings.BEBOT_DB["DB_NAME"],
                               user=settings.BEBOT_DB["DB_USER"],
                               password=settings.BEBOT_DB["DB_PASS"],
                               host=settings.BEBOT_DB["DB_HOST"],
                               port=settings.BEBOT_DB["DB_PORT"])

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Log(BaseModel):
    uid = peewee.IntegerField()
    username = peewee.CharField(max_length=20)
    update_id = peewee.IntegerField()
    text = peewee.CharField(max_length=settings.TEXT)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "logs"

class Game(BaseModel):
    owner_id = peewee.IntegerField()
    owner = peewee.CharField(max_length=20)
    roles = ArrayField(peewee.CharField, default=strings.DEFAULT_ROLE)
    days = peewee.IntegerField(null=True)
    hostages = peewee.CharField(max_length=20, null=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "games"

class Guest(BaseModel):
    game_id = peewee.IntegerField()
    player_id = peewee.IntegerField()
    player = peewee.CharField(max_length=20)
    role = peewee.CharField(max_length=20, null=True)
    room = peewee.BooleanField(null=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "guests"

class Share(BaseModel):
    game_id = peewee.IntegerField()
    from_id = peewee.IntegerField()
    to_id = peewee.IntegerField(null=True)
    role = peewee.BooleanField()
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "shares"

class Quiz(BaseModel):
    answer = peewee.CharField(max_length=1)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "quiz"

class Response(BaseModel):
    question = peewee.IntegerField()
    player_id = peewee.IntegerField()
    player = peewee.CharField(max_length=20)
    response = peewee.CharField(max_length=1)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "responses"

#db.drop_tables([Log], safe=True)
#db.drop_tables([Game], safe=True)
#db.drop_tables([Guest], safe=True)
#db.drop_tables([Share], safe=True)
db.drop_tables([Quiz], safe=True)
db.drop_tables([Response], safe=True)

db.create_tables([Log], safe=True)
db.create_tables([Game], safe=True)
db.create_tables([Guest], safe=True)
db.create_tables([Share], safe=True)
db.create_tables([Quiz], safe=True)
db.create_tables([Response], safe=True)

Quiz.create(answer="b") #Q1
Quiz.create(answer="c") #Q2
Quiz.create(answer="c") #Q3
Quiz.create(answer="c") #Q4
Quiz.create(answer="b") #Q5
Quiz.create(answer="a") #Q6
Quiz.create(answer="a") #Q7
Quiz.create(answer="b") #Q8
Quiz.create(answer="a") #Q9
Quiz.create(answer="a") #Q10
Quiz.create(answer="a") #Q11
Quiz.create(answer="c") #Q12
Quiz.create(answer="b") #Q13
Quiz.create(answer="c") #Q14
Quiz.create(answer="a") #Q15
Quiz.create(answer="a") #Q16
Quiz.create(answer="a") #Q17
Quiz.create(answer="c") #Q18
Quiz.create(answer="a") #Q19
Quiz.create(answer="b") #Q20
Quiz.create(answer="b") #Q21
Quiz.create(answer="c") #Q22
Quiz.create(answer="b") #Q23
