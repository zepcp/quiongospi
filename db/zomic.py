import settings

import peewee
import time

db = peewee.PostgresqlDatabase(settings.ZOMIC_DB["DB_NAME"],
                               user=settings.ZOMIC_DB["DB_USER"],
                               password=settings.ZOMIC_DB["DB_PASS"],
                               host=settings.ZOMIC_DB["DB_HOST"],
                               port=settings.ZOMIC_DB["DB_PORT"])

def get_where_condition(table, id=None, genesis=None, active=None, name=None,
                        email=None, wallet=None, chat_id=None, proposal=None,
                        description=None, username=None, username_exists=None):
    return (table.id == id if id else True) & \
           (table.genesis == genesis if genesis else True) & \
           (table.active == active if active else True) & \
           (table.name.contains(name) if name else True) & \
           (table.email == email if email else True) & \
           (table.wallet == wallet if wallet else True) & \
           (table.chat_id == chat_id if chat_id else True) & \
           (table.proposal == proposal if proposal else True) & \
           (table.description.contains(description) if description else True) & \
           (table.username == username if username else True) & \
           (table.username != None if username_exists else True)

def get_lines(query, member=None, rule=None, proposal=None):
    result = []
    for line in query:
        json = {}
        json['id'] = line.id
        json['genesis'] = line.genesis
        json['active'] = line.active

        if member:
            json['name'] = line.name
            json['email'] = line.email
            json['wallet'] = line.wallet
            json['points'] = line.points
            json['balance'] = line.balance

        if rule or proposal:
            json['description'] = line.description

        if proposal:
            json['username'] = line.username

        result.append(json)
    return result

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Genesis(BaseModel):
    genesis = peewee.IntegerField(index=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "genesis"

class Members(BaseModel):
    genesis = peewee.IntegerField(index=True)
    chat_id = peewee.IntegerField(default=0)
    name = peewee.CharField(max_length=settings.NAME)
    email = peewee.CharField(max_length=settings.NAME, null=True)
    wallet = peewee.CharField(max_length=settings.WALLET, null=True)
    points = peewee.IntegerField(default=0)
    balance = peewee.IntegerField(default=0)
    active = peewee.BooleanField(default=True, index=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "members"

class Rules(BaseModel):
    genesis = peewee.IntegerField(index=True)
    chat_id = peewee.IntegerField(default=0)
    description = peewee.CharField(max_length=settings.TEXT)
    votes = peewee.IntegerField(default=0)
    rate = peewee.IntegerField(default=50)
    active = peewee.BooleanField(default=True, index=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "rules"

class Proposals(BaseModel):
    genesis = peewee.IntegerField(index=True)
    chat_id = peewee.IntegerField()
    username = peewee.CharField(max_length=settings.NAME, null=True)
    description = peewee.CharField(max_length=settings.TEXT)
    active = peewee.BooleanField(default=True, index=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "proposals"

class Votes(BaseModel):
    chat_id = peewee.IntegerField()
    proposal = peewee.IntegerField(index=True)
    vote = peewee.IntegerField()
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "votes"

class Taxes(BaseModel):
    genesis = peewee.IntegerField(index=True)
    chat_id = peewee.IntegerField()
    txid = peewee.CharField(max_length=settings.TXID, index=True)
    amount = peewee.IntegerField(default=0)
    description = peewee.CharField(max_length=settings.TEXT)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "taxes"

class Telegram(BaseModel):
    chat_id = peewee.IntegerField()
    update_id = peewee.IntegerField()
    text = peewee.CharField(max_length=settings.TEXT, index=True)
    date = peewee.IntegerField(default=int(time.time()))

    class Meta:
        db_table = "telegram"

db.create_tables([Genesis], safe=True)
db.create_tables([Members], safe=True)
db.create_tables([Rules], safe=True)
db.create_tables([Proposals], safe=True)
db.create_tables([Votes], safe=True)
db.create_tables([Taxes], safe=True)
db.create_tables([Telegram], safe=True)

# Initialize Genesis Block (Block Timestamp)
if Genesis.select().count() == 0:
    Genesis.create(genesis = 0)

# Initialize Genesis Block (Founders)
if Members.select().count() == 0:
    for founder in settings.GENESIS_MEMBERS:
        Members.create(genesis = 0, name = founder)

# Initialize Genesis Block (Initial Rules)
if Rules.select().count() == 0:
    for rule in settings.GENESIS_RULES:
        Rules.create(genesis = 0, description = rule)

