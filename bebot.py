import random
import time
import unidecode
import logging
import peewee

import settings
from utils import telegram
from db import bebot as db
from strings import bebot as strings

LOGGER = logging.getLogger("bebot")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt=settings.DATETIME)

if settings.DEBUG:
    LOGGER.setLevel(logging.DEBUG)

def list_cards(groom=True, bride=True, neutral=True, name=False):
    cards = []
    for character in strings.CHARACTERS:
        if not bride and strings.CHARACTERS[character]["team"] == strings.TEAM_CAROL_STICKER:
            continue
        if not groom and strings.CHARACTERS[character]["team"] == strings.TEAM_BE_STICKER:
            continue
        if not neutral and strings.CHARACTERS[character]["team"] == strings.NO_TEAM_STICKER:
            continue
        info = strings.CHARACTERS[character]
        if not name:
            cards.append(character+" - "+info["goal"])
        else:
            cards.append(character+" - "+info["name"])
    return "\n".join(cards)

def card_details(character):
    info = strings.CHARACTERS[character]
    details = "Name: " + info["name"]
    details += "\nGoal: " + info["goal"]
    details += "\nRecommended with: " + str(info["with"])[1:-1]
    return details, info["sticker"], info["team"]

def room_distribution(game_id):
    room_0 = []
    room_1 = []
    guestlist = db.Guest.select().where(db.Guest.game_id == game_id)
    for guest in guestlist:
        if guest.room:
            room_1.append(guest.player)
        else:
            room_0.append(guest.player)
    return room_0, room_1

def new(uid, game, username):
    if game:
        telegram.send_message(strings.ALREADY_NEW, uid, bot="bebot")
        return

    game = db.Game.create(owner_id=uid, owner=username)
    db.Guest.create(game_id=game.id, player_id=uid, player=username)
    telegram.send_message(strings.NEW, uid, bot="bebot")

def guestlist(uid, text, game):
    if not game:
        gamelist = db.Game.select()
        if not gamelist.exists():
            telegram.send_message(strings.NO_WEDDING_AVAILABLE, uid, bot="bebot")
            return

        games_msg = ""
        for game in gamelist:
            if text == "/guestlist_"+game.owner:
                break
            games_msg += "\n/guestlist_"+game.owner

        if text != "/guestlist_"+game.owner:
            telegram.send_message(strings.WHICH_GUESTLIST % games_msg, uid, bot="bebot")
            return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()
    room_0, room_1 = room_distribution(game.id)
    msg = strings.GUESTLIST % (invites, accepted, game.roles, room_0, room_1)
    telegram.send_message(msg, uid, bot="bebot")

def add(text, game):
    if text not in game.roles:
        db.Game.update(roles=peewee.fn.array_append(db.Game.roles, text)
                      ).where(db.Game.id == game.id).execute()
        telegram.send_message(strings.ADDED % text, game.owner_id, bot="bebot")
        return
    db.Game.update(roles=peewee.fn.array_remove(db.Game.roles, text)
                  ).where(db.Game.id == game.id).execute()
    telegram.send_message(strings.REMOVED % text, game.owner_id, bot="bebot")

def delete(uid, game):
    if not game:
        telegram.send_message(strings.NO_WEDDING_PLANNED, uid, bot="bebot")
        return

    db.Game.delete().where(db.Game.id == game.id).execute()
    db.Guest.delete().where(db.Guest.game_id == game.id).execute()
    db.Share.delete().where(db.Share.game_id == game.id).execute()
    telegram.send_message(strings.DELETED, uid, bot="bebot")

def party(uid, game):
    if not game:
        telegram.send_message(strings.NO_WEDDING_PLANNED, uid, bot="bebot")
        return

    if game.days:
        telegram.send_message(strings.ALREADY_PARTYING, uid, bot="bebot")
        return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()

    if accepted < invites - 1 or accepted <= 5:
        telegram.send_message(strings.CANT_PARTY, uid, bot="bebot")
        return

    days = 3 if accepted <= 10 else 5
    hostages = [1, 1, 1]
    hostages = [2, 2, 2, 1, 1] if 10 < accepted <= 13 else hostages
    hostages = [3, 2, 2, 1, 1] if 13 < accepted <= 17 else hostages
    hostages = [4, 3, 2, 1, 1] if 17 < accepted <= 21 else hostages
    hostages = [5, 4, 3, 2, 1] if 21 < accepted else hostages

    db.Game.update(days=days, hostages=hostages).where(db.Game.id == game.id).execute()

    rooms = []
    for iterate in range(accepted):
        rooms.append(iterate % 2)

    roles = game.roles
    team_card = True if strings.NEED_TEAM_ROLE in game.roles else False

    for guest in db.Guest.select().where(db.Guest.game_id == game.id):
        role = random.choice(roles) if len(roles) != 2 or strings.LAST_DAY_ROLE[0] not in roles \
                                    else strings.LAST_DAY_ROLE[0]
        roles.remove(role)
        starting_room = random.choice(rooms)
        rooms.remove(starting_room)
        db.Guest.update(room=True if starting_room == 1 else False,
                        role=role).where(db.Guest.game_id == game.id,
                                         db.Guest.player_id == guest.player_id).execute()
        _, sticker, team = card_details(role)

        party_msg = strings.PARTY_DETAILS % (days, hostages, starting_room)
        telegram.send_sticker(sticker, guest.player_id, bot="bebot")
        if team_card:
            telegram.send_sticker(team, guest.player_id, bot="bebot")
        telegram.send_message(party_msg, guest.player_id, bot="bebot")

def join(uid, text, username):
    if text == "/join":
        available = db.Game.select().where(db.Game.days == None)
        if not available.exists():
            telegram.send_message(strings.NO_WEDDING_AVAILABLE, uid, bot="bebot")
            return

        join_msg = ""
        for game in available:
            join_msg += "\n/join_"+game.owner

        telegram.send_message(strings.JOIN % join_msg, uid, bot="bebot")
        return

    game = db.Game.select().where(db.Game.owner == text[6:], db.Game.days == None)
    if not game.exists():
        telegram.send_message(strings.GUESTLIST_FULL, uid, bot="bebot")
        return

    game = game.get()

    if db.Guest.select().where(db.Guest.game_id == game.id,
                               db.Guest.player_id == uid).exists():
        db.Guest.delete().where(db.Guest.game_id == game.id,
                                db.Guest.player_id == uid).execute()
        telegram.send_message(strings.LEAVE, uid, bot="bebot")
        return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()
    if invites == accepted:
        telegram.send_message(strings.GUESTLIST_FULL, uid, bot="bebot")
        return

    db.Guest.create(game_id=game.id, player_id=uid, player=username)
    telegram.send_message(strings.JOINED % game.roles, uid, bot="bebot")
    return

def share(uid, text):
    guest = db.Guest.select().where(db.Guest.player_id == uid,
                                    db.Guest.role != None)
    if not guest.exists():
        telegram.send_message(strings.INVALID_SHARE, uid, bot="bebot")
        return

    guest = guest.get()
    guestlist = db.Guest.select().where(db.Guest.game_id == guest.game_id,
                                        db.Guest.room == guest.room,
                                        db.Guest.player_id != uid)

    share_msg = ""
    for guest in guestlist:
        share_msg += "\n/with_"+guest.player

    role = False if text == "/share_team" else True
    if not db.Share.select().where(db.Share.from_id == uid,
                                   db.Share.to_id == None).exists():
        db.Share.create(game_id=guest.game_id, from_id=uid, role=role)
    else:
        db.Share.update(game_id=guest.game_id,
                        role=role).where(db.Share.game_id == guest.game_id,
                                         db.Share.from_id == uid,
                                         db.Share.to_id == None).execute()
    telegram.send_message(strings.SHARE_WITH % share_msg, uid, bot="bebot")

def share_with(uid, text):
    share = db.Share.select().where(db.Share.from_id == uid,
                                    db.Share.to_id == None)
    if not share.exists():
        telegram.send_message(strings.INVALID_WITH, uid, bot="bebot")
        return

    share = share.get()
    player1 = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                    db.Guest.player_id == uid).get()

    guestlist = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                        db.Guest.room == player1.room,
                                        db.Guest.player_id != uid)

    for guest in guestlist:
        if guest.player == text[6:]:
            db.Share.update(to_id=guest.player_id).where(db.Share.id == share.id
                                                        ).execute()
            telegram.send_message(strings.MUTUAL, uid, bot="bebot")
            return
    telegram.send_message(strings.INVALID_WITH, uid, bot="bebot")
    return

def share_back(uid, text):
    share = db.Share.select().where(db.Share.from_id == uid,
                                    db.Share.to_id != None
                                    ).order_by(db.Share.date.desc())
    if not share.exists():
        telegram.send_message(strings.INVALID_WITH, uid, bot="bebot")
        return

    share = share.get()

    player1 = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                    db.Guest.player_id == uid).get()

    if text == "/no":
        _, role_sticker, team_sticker = card_details(player1.role)
        sticker = role_sticker if share.role else team_sticker

        telegram.send_message(strings.RECEIVED % (player1.player), share.to_id, bot="bebot")
        telegram.send_sticker(sticker, share.to_id, bot="bebot")
        db.Share.delete().where(db.Share.id == share.id).execute()
        return

    if share.role:
        player2 = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                         db.Guest.player_id == share.to_id).get()

        if player2.role in strings.AUTO_ACCEPT_ROLE:
            share_response(player2.player_id, "/accept_"+player1.player)
            return

    share_type = "/share_role" if share.role else "/share_team"
    telegram.send_message(strings.ACCEPT % (share_type, player1.player, player1.player),
                          share.to_id, bot="bebot")
    return

def share_response(uid, text):
    inviter = db.Guest.select().where(db.Guest.player == text[8:])
    if not inviter.exists():
        telegram.send_message(strings.INVALID_MUTUAL, uid, bot="bebot")
        return

    inviter = inviter.get()
    share = db.Share.select().where(db.Share.to_id == uid,
                                    db.Share.from_id == inviter.player_id
                                   ).order_by(db.Share.date.desc())
    if not share.exists():
        telegram.send_message(strings.INVALID_MUTUAL, uid, bot="bebot")
        return

    share = share.get()

    if text == "/reject":
        telegram.send_message(strings.REJECTED, share.from_id, bot="bebot")
        db.Share.delete().where(db.Share.id == share.id).execute()
        return

    player1 = db.Guest.select().where(db.Guest.player_id == share.from_id
                                     ).order_by(db.Guest.date.desc()).get()

    player2 = db.Guest.select().where(db.Guest.player_id == uid
                                     ).order_by(db.Guest.date.desc()).get()

    _, role_sticker, team_sticker = card_details(player1.role)
    sticker1 = role_sticker if share.role else team_sticker

    _, role_sticker, team_sticker = card_details(player2.role)
    sticker2 = role_sticker if share.role else team_sticker

    if share.role:
        if player1.role in strings.SWAPPABLE_ROLE or player2.role in strings.SWAPPABLE_ROLE:
            telegram.send_message(strings.GOT_SWAPPED, player1.player_id, bot="bebot")
            telegram.send_sticker(sticker2, player1.player_id, bot="bebot")
            telegram.send_message(strings.GOT_SWAPPED, player2.player_id, bot="bebot")
            telegram.send_sticker(sticker1, player2.player_id, bot="bebot")
            db.Guest.update(role=player1.role).where(db.Guest.id == player2.id).execute()
            db.Guest.update(role=player2.role).where(db.Guest.id == player1.id).execute()
            db.Share.delete().where(db.Share.id == share.id).execute()
            return

    telegram.send_message(strings.SHARED % (player2.player), player1.player_id, bot="bebot")
    telegram.send_sticker(sticker2, player1.player_id, bot="bebot")
    telegram.send_message(strings.SHARED % (player1.player), player2.player_id, bot="bebot")
    telegram.send_sticker(sticker1, player2.player_id, bot="bebot")
    db.Share.delete().where(db.Share.id == share.id).execute()
    return

def hostages(uid, text, game):
    if not game:
        telegram.send_message(strings.NO_WEDDING_PLANNED, uid, bot="bebot")
        return

    if not game.days:
        telegram.send_message(strings.NO_HOSTAGES, uid, bot="bebot")
        return

    if text == "/hostages":
        db.Share.delete().where(db.Share.game_id == game.id).execute()
        room_0, room_1 = room_distribution(game.id)

        msg_hostages = "0:"
        for hostage in room_0:
            msg_hostages += "\n/hostage_"+hostage
        telegram.send_message(strings.HOSTAGES % msg_hostages, game.owner_id, bot="bebot")

        msg_hostages = "1:"
        for hostage in room_1:
            msg_hostages += "\n/hostage_"+hostage
        telegram.send_message(strings.HOSTAGES % msg_hostages, game.owner_id, bot="bebot")
        return

    hostage = text[9:]
    db.Guest.update(room=True if db.Guest.room == False else False,
                   ).where(db.Guest.game_id == game.id,
                           db.Guest.player == hostage).execute()
    return

def last(uid, game):
    if game:
        if strings.LAST_DAY_ROLE[0] not in game.roles:
            telegram.send_message(strings.INVALID_LAST, uid, bot="bebot")
            return

        for role in game.roles:
            if not db.Guest.select().where(db.Guest.game_id == game.id,
                                           db.Guest.role == role).exists():
                break

        player = db.Guest.select().where(db.Guest.game_id == game.id,
                                         db.Guest.role == strings.LAST_DAY_ROLE[0]).get()

        _, sticker, _ = card_details(role)
        telegram.send_sticker(sticker, player.player_id, bot="bebot")
        return

    last_day_role = db.Guest.select().where(db.Guest.player_id == uid
                                           ).order_by(db.Guest.date.desc())

    if last_day_role.exists():
        last_day_role = last_day_role.get()
        if last_day_role.role in strings.LAST_DAY_ROLE:
            game = db.Game.select().where(db.Game.id == last_day_role.game_id).get()
            telegram.send_message(strings.LAST, game.owner_id, bot="bebot")
            return

    telegram.send_message(strings.INVALID_LAST, uid, bot="bebot")
    return

def root(uid, text):
    if uid == 546114127 and text == "/root_clean_all":
        db.Game.delete().execute()
        db.Guest.delete().execute()
        db.Share.delete().execute()
        return
    if uid == 546114127 and text == "/root_clean_shares":
        db.Share.delete().execute()
        return
    return

def process_msg(uid, text, game, username):
    if text == "/start":
        telegram.send_sticker(strings.START_STICKER, uid, bot="bebot")
        telegram.send_message(strings.START, uid, bot="bebot")

    elif text == "/help":
        telegram.send_message(strings.HELP, uid, bot="bebot")

    elif text == "/rules":
        telegram.send_message(strings.RULES, uid, bot="bebot")

    elif text == "/guests":
        telegram.send_message(list_cards(), uid, bot="bebot")

    elif text == "/guests_groom":
        telegram.send_message(list_cards(bride=False, neutral=False), uid, bot="bebot")

    elif text == "/guests_bride":
        telegram.send_message(list_cards(groom=False, neutral=False), uid, bot="bebot")

    elif text == "/guests_neutral":
        telegram.send_message(list_cards(groom=False, bride=False), uid, bot="bebot")

    elif text == "/guests_short":
        telegram.send_message(str(list(strings.CHARACTERS)), uid, bot="bebot")

    elif text == "/guests_name":
        telegram.send_message(list_cards(name=True), uid, bot="bebot")

    elif text[:9] == "/template":
        if text in strings.TEMPLATES:
            telegram.send_message(str(strings.TEMPLATES[text]["roles"]), uid, bot="bebot")
        else:
            telegram.send_message(str(list(strings.TEMPLATES)), uid, bot="bebot")

    elif text == "/new":
        new(uid, game, username)

    elif text[:10] == "/guestlist":
        guestlist(uid, text, game)

    elif text in strings.CHARACTERS:
        if not game or game.days:
            _, sticker, _ = card_details(text)
            telegram.send_sticker(sticker, uid, bot="bebot")
            return
        add(text, game)

    elif text == "/delete":
        delete(uid, game)

    elif text == "/party":
        party(uid, game)

    elif text[:5] == "/join":
        join(uid, text, username)

    elif text[:6] == "/share":
        share(uid, text)

    elif text[:6] == "/with_":
        share_with(uid, text)

    elif text in ("/yes", "/no"):
        share_back(uid, text)

    elif text[:8] in ("/accept_", "/reject_"):
        share_response(uid, text)

    elif text[:8] == "/hostage":
        hostages(uid, text, game)

    elif text == "/last":
        last(uid, game)

    elif text[:5] == "/root":
        root(uid, text)

    else:
        LOGGER.error('COULDNT UNDERSTAND %s', text)
        telegram.send_message(strings.BAD_REQUEST, uid, bot="bebot")

def last_msg():
    last_msg = db.Log.select(peewee.fn.MAX(db.Log.update_id)).get().max
    return last_msg if last_msg is not None else settings.TELEGRAM_OFFSET

def get_username(msg):
    try:
        return unidecode.unidecode(msg["from"]["username"].lower())
    except KeyError:
        return unidecode.unidecode(msg["from"]["first_name"].lower())

if __name__ == "__main__":
    LAST_MSG = last_msg()
    STARTED = time.time()
    UPDATE_ID = 0
    while True:
        for msg in telegram.get_messages(UPDATE_ID, bot="bebot"):
            if STARTED > msg["message"]["date"]:
                continue
            UPDATE_ID = msg["update_id"]

            if UPDATE_ID <= LAST_MSG:
                continue

            try:
                uid = msg["message"]["from"]["id"]
                text = msg["message"]["text"]
                username = get_username(msg["message"])
            except KeyError:
                try:
                    uid = msg["edited_message"]["from"]["id"]
                    text = msg["edited_message"]["text"]
                    username = get_username(msg["edited_message"])
                except KeyError:
                    LOGGER.error('COULDNT READ %s', msg)
                    continue

            game = db.Game.select().where(db.Game.owner_id == uid)
            game = game.get() if game.exists() else None
            db.Log.create(uid=uid,
                          username=username,
                          update_id=UPDATE_ID,
                          text=text)

            LOGGER.debug(uid, text, game, username)
            process_msg(uid, text, game, username)

        LAST_MSG = UPDATE_ID
        time.sleep(settings.TELEGRAM_SLEEP)
