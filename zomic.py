import logging
import time
from peewee import fn

import settings
from utils import telegram
from utils import types
from db import zomic as db
from strings import zomic as strings

logger = logging.getLogger('zomic')

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt=settings.DATETIME)

if settings.DEBUG:
    logger.setLevel(logging.DEBUG)

def last_msg():
    last_msg = db.Telegram.select(fn.MAX(db.Telegram.update_id)).get().max
    return last_msg if last_msg is not None else settings.TELEGRAM_OFFSET

def genesis():
    return db.Genesis.select(fn.MAX(db.Genesis.genesis)).get().max

def vote_number(vote):
    if vote == "upvote":
        return 1
    elif vote == "downvote":
        return -1
    return 0

def update_info(user, info):
    wallet = None
    email = None
    try:
        wallet = types.wallet(info)
    except Exception as exception:
        try:
            email = types.email(info)
        except Exception as exception:
            telegram.send_message(strings.BAD_REQUEST, user)
            return False

    if wallet:
        db.Members.update(wallet=wallet).where(db.get_where_condition(
                                               db.Members,
                                               chat_id=user)).execute()

    if email:
        db.Members.update(email=email).where(db.get_where_condition(
                                             db.Members,
                                             chat_id=user)).execute()

    return telegram.send_message(strings.SUCCESS, user)

def propose(user, description):
    if description == "":
        telegram.send_message(strings.NOT_FOUND, user)
        return False

    if db.Proposals.select().where(db.get_where_condition(
                                   db.Proposals,
                                   genesis = genesis(),
                                   chat_id = user,
                                   active = True,
                                   username = None)).count() > 0:
        telegram.send_message(strings.CONFLICT, user)
        return False

    db.Proposals.create(genesis = genesis(),
                        chat_id = user,
                        description = description)
    return telegram.send_message(strings.SUCCESS, user)

def invite(user, info):
    try:
        username = info.split(" ")[0]
        description = info.split(" ")[1:]

        if username == "":
            raise ValueError()

        if db.Proposals.select().where(db.get_where_condition(
                                       db.Proposals,
                                       genesis = genesis(),
                                       chat_id = user,
                                       active = True,
                                       username_exists = True)).count() > 0:
            telegram.send_message(strings.CONFLICT, user)
            return False

        db.Proposals.create(genesis = genesis(),
                            chat_id = user,
                            username = username,
                            description = " ".join(description))
        return telegram.send_message(strings.SUCCESS, user)
    except:
        telegram.send_message(strings.BAD_REQUEST, user)
        return False

def vote(user, info):
    try:
        [vote_id, vote] = info.split(" ")
        if vote.lower() not in ("upvote", "downvote"):
            raise ValueError()

        if db.Proposals.select().where(db.get_where_condition(
                                       db.Proposals,
                                       id = vote_id,
                                       active = True)).count() == 0:
            telegram.send_message(strings.NOT_FOUND, user)
            return False

        if db.Votes.select().where(db.get_where_condition(
                                   db.Votes,
                                   chat_id = user,
                                   proposal = vote_id)).count() > 0:
            telegram.send_message(strings.CONFLICT, user)
            return False

        db.Votes.create(chat_id = user,
                        proposal = vote_id,
                        vote = vote_number(vote.lower()))

        return telegram.send_message(strings.SUCCESS, user)
    except:
        telegram.send_message(strings.BAD_REQUEST, user)
        return False

def quit(user, wallet = None):
    if wallet is not None:
        try:
            wallet = types.wallet(wallet)
        except Exception as exception:
            telegram.send_message(exception, user)
            telegram.send_message(strings.RAGE_QUIT, user)
            return False

    db.Members.update(active=False).where(db.get_where_condition(
                                          db.Members,
                                          chat_id=user)).execute()
    # /quit
    if wallet:
        telegram.send_message(strings.QUIT % wallet, user)
    # /rage_quit
    else:
        telegram.send_message(strings.QUIT.split("\n")[0], user)

    return telegram.send_message(strings.SUCCESS, user)

def process_msg(user, text):
    if text == "/start":
        telegram.send_message(strings.START, user)

    elif text[0:7] == "/update":
        update_info(user, text[8:])

    elif text[0:8] == "/propose":
        propose(user, text[9:])

    elif text[0:7] == "/invite":
        invite(user, text[8:])

    elif text[0:5] == "/vote":
        vote(user, text[6:])

    elif text[0:5] == "/remove":
        print('TODO inactivate vote or proposal')

    elif text[0:5] == "/quit":
        quit(user, text[6:])

    elif text[0:11] == "/rage_quit":
        quit(user)

    elif text == "/kill" and user == 546114127:
        exit()

    elif text == "/genesis" and user == 546114127:
        print('TODO: make proposals rules or usernames members if active and passed votation')
        print('TODO: make proposals of past genesis inactives')
        print('TODO: recount points')

if __name__ == "__main__":
    last_msg = last_msg()
    update_id = 0
    while True:
        for msg in telegram.get_messages(update_id):
            update_id = msg["update_id"]
            try:
                user = msg["message"]["from"]["id"]
                username = msg["message"]["from"]["username"]
                text = msg["message"]["text"]
            except:
                try:
                    user = msg["edited_message"]["from"]["id"]
                    username = msg["edited_message"]["from"]["username"]
                    text = msg["edited_message"]["text"]
                except:
                    logger.error('COULDNT READ %s' % msg)

            #Msg Already Processed
            if update_id <= last_msg:
                continue

            db.Telegram.create(chat_id = user,
                               update_id = update_id,
                               text = text)

            #New Member
            if db.Members.select().where(db.get_where_condition(
                                         db.Members,
                                         name=username,
                                         chat_id=0,
                                         active=True)):
                first_name = msg["message"]["from"]["first_name"]
                last_name = msg["message"]["from"]["last_name"]
                name = first_name + " " + last_name
                db.Members.update(name=name, 
                                  chat_id=user).where(db.get_where_condition(
                                                      db.Members,
                                                      name=username,
                                                      chat_id=0,
                                                      active=True)).execute()

            #Not An Active Member
            if not db.Members.select().where(db.get_where_condition(
                                             db.Members,
                                             chat_id=user,
                                             active=True)):
                telegram.send_message(strings.NOT_MEMBER, user)
            else:
                process_msg(user, text)

        last_msg = update_id
        time.sleep(settings.TELEGRAM_SLEEP)

