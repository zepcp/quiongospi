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

#db.drop_tables([Log], safe=True)
#db.drop_tables([Game], safe=True)
#db.drop_tables([Guest], safe=True)
#db.drop_tables([Share], safe=True)

db.create_tables([Log], safe=True)
db.create_tables([Game], safe=True)
db.create_tables([Guest], safe=True)
db.create_tables([Share], safe=True)
