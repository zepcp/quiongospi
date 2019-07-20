import random
import time
import unidecode
import logging
import peewee

import settings
from utils.telegram import BOT
from db import bebot as db
from strings import bebot as strings

LOGGER = logging.getLogger("bebot")

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] %(message)s',
                    datefmt=settings.DATETIME)

if settings.DEBUG:
    LOGGER.setLevel(logging.DEBUG)

BEBOT = BOT()

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
        BEBOT.send(uid, strings.ALREADY_NEW)
        return

    game = db.Game.create(owner_id=uid, owner=username)
    db.Guest.create(game_id=game.id, player_id=uid, player=username)
    BEBOT.send(uid, strings.NEW)

def guestlist(uid, text, game):
    if not game:
        gamelist = db.Game.select()
        if not gamelist.exists():
            BEBOT.send(uid, strings.NO_WEDDING_AVAILABLE)
            return

        games_msg = ""
        for game in gamelist:
            if text == "/guestlist_"+game.owner:
                break
            games_msg += "\n/guestlist_"+game.owner

        if text != "/guestlist_"+game.owner:
            BEBOT.send(uid, strings.WHICH_GUESTLIST % games_msg)
            return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()
    room_0, room_1 = room_distribution(game.id)
    BEBOT.send(uid, strings.GUESTLIST % (invites, accepted, game.roles, room_0, room_1))

def add(text, game):
    if text not in game.roles:
        db.Game.update(roles=peewee.fn.array_append(db.Game.roles, text)
                      ).where(db.Game.id == game.id).execute()
        BEBOT.send(game.owner_id, strings.ADDED % text)
        return
    db.Game.update(roles=peewee.fn.array_remove(db.Game.roles, text)
                  ).where(db.Game.id == game.id).execute()
    BEBOT.send(game.owner_id, strings.REMOVED % text)

def delete(uid, game):
    if not game:
        BEBOT.send(uid, strings.NO_WEDDING_PLANNED)
        return

    db.Game.delete().where(db.Game.id == game.id).execute()
    db.Guest.delete().where(db.Guest.game_id == game.id).execute()
    db.Share.delete().where(db.Share.game_id == game.id).execute()
    BEBOT.send(uid, strings.DELETED)

def party(uid, game):
    if not game:
        BEBOT.send(uid, strings.NO_WEDDING_PLANNED)
        return

    if game.days:
        BEBOT.send(uid, strings.ALREADY_PARTYING)
        return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()

    if accepted < invites - 1 or accepted < 2:
        BEBOT.send(uid, strings.CANT_PARTY)
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
        BEBOT.send(guest.player_id, party_msg, sticker)

def join(uid, text, username):
    if text == "/join":
        available = db.Game.select().where(db.Game.days == None)
        if not available.exists():
            BEBOT.send(uid, strings.NO_WEDDING_AVAILABLE)
            return

        join_msg = ""
        for game in available:
            join_msg += "\n/join_"+game.owner

        BEBOT.send(uid, strings.JOIN % join_msg)
        return

    game = db.Game.select().where(db.Game.owner == text[6:], db.Game.days == None)
    if not game.exists():
        BEBOT.send(uid, strings.GUESTLIST_FULL)
        return

    game = game.get()

    if db.Guest.select().where(db.Guest.game_id == game.id,
                               db.Guest.player_id == uid).exists():
        db.Guest.delete().where(db.Guest.game_id == game.id,
                                db.Guest.player_id == uid).execute()
        BEBOT.send(uid, strings.LEAVE)
        return

    invites = len(game.roles) if strings.LAST_DAY_ROLE[0] not in game.roles else len(game.roles) - 1
    accepted = db.Guest.select().where(db.Guest.game_id == game.id).count()
    if invites == accepted:
        BEBOT.send(uid, strings.GUESTLIST_FULL)
        return

    db.Guest.create(game_id=game.id, player_id=uid, player=username)
    BEBOT.send(uid, strings.JOINED % game.roles)
    return

def share(uid, text):
    guest = db.Guest.select().where(db.Guest.player_id == uid,
                                    db.Guest.role != None)
    if not guest.exists():
        BEBOT.send(uid, strings.INVALID_SHARE)
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
    BEBOT.send(uid, strings.SHARE_WITH % share_msg)

def share_with(uid, text):
    share = db.Share.select().where(db.Share.from_id == uid,
                                    db.Share.to_id == None)
    if not share.exists():
        BEBOT.send(uid, strings.INVALID_WITH)
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
            BEBOT.send(uid, strings.MUTUAL)
            return
    BEBOT.send(uid, strings.INVALID_WITH)
    return

def share_back(uid, text):
    share = db.Share.select().where(db.Share.from_id == uid,
                                    db.Share.to_id != None
                                    ).order_by(db.Share.date.desc())
    if not share.exists():
        BEBOT.send(uid, strings.INVALID_WITH)
        return

    share = share.get()

    player1 = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                    db.Guest.player_id == uid).get()

    if text == "/no":
        _, role_sticker, team_sticker = card_details(player1.role)
        sticker = role_sticker if share.role else team_sticker

        BEBOT.send(share.to_id, strings.RECEIVED % player1.player, sticker)
        db.Share.delete().where(db.Share.id == share.id).execute()
        return

    if share.role:
        player2 = db.Guest.select().where(db.Guest.game_id == share.game_id,
                                         db.Guest.player_id == share.to_id).get()

        if player2.role in strings.AUTO_ACCEPT_ROLE:
            share_response(player2.player_id, "/accept_"+player1.player)
            return

    share_type = "/share_role" if share.role else "/share_team"
    BEBOT.send(share.to_id, strings.ACCEPT % (share_type, player1.player, player1.player))
    return

def share_response(uid, text):
    inviter = db.Guest.select().where(db.Guest.player == text[8:])
    if not inviter.exists():
        BEBOT.send(uid, strings.INVALID_MUTUAL)
        return

    inviter = inviter.get()
    share = db.Share.select().where(db.Share.to_id == uid,
                                    db.Share.from_id == inviter.player_id
                                   ).order_by(db.Share.date.desc())
    if not share.exists():
        BEBOT.send(uid, strings.INVALID_MUTUAL)
        return

    share = share.get()

    if text[:8] == "/reject_":
        BEBOT.send(share.from_id, strings.REJECTED)
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
            BEBOT.send(player1.player_id, strings.GOT_SWAPPED, sticker2)
            BEBOT.send(player2.player_id, strings.GOT_SWAPPED, sticker1)
            db.Guest.update(role=player1.role).where(db.Guest.id == player2.id).execute()
            db.Guest.update(role=player2.role).where(db.Guest.id == player1.id).execute()
            db.Share.delete().where(db.Share.id == share.id).execute()
            return

    BEBOT.send(player1.player_id, strings.SHARED % (player2.player), sticker2)
    BEBOT.send(player2.player_id, strings.SHARED % (player1.player), sticker1)
    db.Share.delete().where(db.Share.id == share.id).execute()
    return

def hostages(uid, text, game):
    if not game:
        BEBOT.send(uid, strings.NO_WEDDING_PLANNED)
        return

    if not game.days:
        BEBOT.send(uid, strings.NO_HOSTAGES)
        return

    if text == "/hostages":
        db.Share.delete().where(db.Share.game_id == game.id).execute()
        room_0, room_1 = room_distribution(game.id)

        msg_hostages = "0:"
        for hostage in room_0:
            msg_hostages += "\n/hostage_"+hostage
        BEBOT.send(game.owner_id, strings.NO_HOSTAGES % msg_hostages)

        msg_hostages = "1:"
        for hostage in room_1:
            msg_hostages += "\n/hostage_"+hostage
        BEBOT.send(game.owner_id, strings.NO_HOSTAGES % msg_hostages)
        return

    hostage = text[9:]
    room = db.Guest.select().where(db.Guest.game_id == game.id,
                                   db.Guest.player == hostage)

    if room:
        room = False if room.get().room else True
        db.Guest.update(room=room,
                       ).where(db.Guest.game_id == game.id,
                               db.Guest.player == hostage).execute()
    return

def last(uid, game):
    if game:
        if strings.LAST_DAY_ROLE[0] not in game.roles:
            BEBOT.send(uid, strings.INVALID_LAST)
            return

        for role in game.roles:
            if not db.Guest.select().where(db.Guest.game_id == game.id,
                                           db.Guest.role == role).exists():
                break

        player = db.Guest.select().where(db.Guest.game_id == game.id,
                                         db.Guest.role == strings.LAST_DAY_ROLE[0]).get()

        db.Guest.update(role=role).where(db.Guest.game_id == game.id,
                                         db.Guest.player_id == player.player_id).execute()

        _, sticker, _ = card_details(role)
        BEBOT.send(player.player_id, sticker=sticker)
        return

    last_day_role = db.Guest.select().where(db.Guest.player_id == uid
                                           ).order_by(db.Guest.date.desc())

    if last_day_role.exists():
        last_day_role = last_day_role.get()
        if last_day_role.role in strings.LAST_DAY_ROLE:
            game = db.Game.select().where(db.Game.id == last_day_role.game_id).get()
            BEBOT.send(game.owner_id, strings.LAST)
            return

    BEBOT.send(uid, strings.INVALID_LAST)
    return

def root(uid, text):
    if uid == 546114127 and text == "/root_clean_games":
        db.Game.delete().execute()
        db.Guest.delete().execute()
        db.Share.delete().execute()
        return
    if uid == 546114127 and text == "/root_clean_answers":
        db.Response.delete().execute()
        return
    if uid == 546114127 and text == "/root_clean_shares":
        db.Share.delete().execute()
        return
    return

def quiz(uid, username, question, answer):
    last_response = db.Response.select().order_by(db.Response.question.desc())
    if last_response.exists():
        if last_response.get().question > question:
            BEBOT.send(uid, "Sorry we are already on question %d" % last_response.get().question)
            return

        if last_response.get().question < question + 1:
            BEBOT.send(uid, "Sorry we are still on question %d" % last_response.get().question)
            return
    else:
        if question != 1:
            BEBOT.send(uid, "Sorry we are still on question 1")
            return

    already_answered = db.Response.select().where(db.Response.question == question,
                                                  db.Response.player_id == uid)
    if already_answered.exists():
        BEBOT.send(uid, "Sorry you have already answered this question")
        return

    db.Response.create(question=question, player_id=uid, player=username, response=answer)
    BEBOT.send(uid, "Your answer has been registered")
    return

def quiz_result():
    players = db.Response.select().distinct(db.Response.player_id)

    winner = []
    win_points = 0
    for player in players:
        responses = db.Response.select().where(db.Response.player_id == player.player_id)
        result = 0
        correct = []
        for each in responses:
            question = db.Quiz.select().where(db.Quiz.id == each.question).get()
            if question.answer == each.response:
                result += 1
                correct.append(each.question)
        BEBOT.send(player.player_id, "Your quiz result was %d" % result)
        BEBOT.send(player.player_id, "Your correct answers were: %s" % str(correct)[1:-1])
        if result > win_points:
            winner = [each.player]
            win_points = result
        elif result == win_points:
            winner.append(each.player)

    for player in players:
        BEBOT.send(player.player_id, "Winner was %s with %d" % (str(winner)[1:-1], win_points))
    return

def process_msg(uid, text, game, username):
    if text == "/start":
        BEBOT.send(uid, strings.START, strings.START_STICKER)

    elif text == "/help":
        BEBOT.send(uid, strings.HELP)

    elif text == "/rules":
        BEBOT.send(uid, strings.RULES)

    elif text == "/guests":
        BEBOT.send(uid, list_cards())

    elif text == "/guests_groom":
        BEBOT.send(uid, list_cards(bride=False, neutral=False))

    elif text == "/guests_bride":
        BEBOT.send(uid, list_cards(groom=False, neutral=False))

    elif text == "/guests_neutral":
        BEBOT.send(uid, list_cards(groom=False, bride=False))

    elif text == "/guests_short":
        BEBOT.send(uid, str(list(strings.CHARACTERS)))

    elif text == "/guests_name":
        BEBOT.send(uid, list_cards(name=True))

    elif text[:9] == "/template":
        if text in strings.TEMPLATES:
            BEBOT.send(uid, str(strings.TEMPLATES[text]["roles"]))
        else:
            BEBOT.send(uid, str(list(strings.TEMPLATES)))

    elif text == "/new":
        new(uid, game, username)

    elif text[:10] == "/guestlist":
        guestlist(uid, text, game)

    elif text in strings.CHARACTERS:
        if not game or game.days:
            _, sticker, _ = card_details(text)
            BEBOT.send(uid, sticker=sticker)
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

    elif text == "/quiz_result":
        quiz_result()

    else:
        try:
            question = int(text[1:-1])
            answer = text[-1]

            if answer in ("a", "b", "c") and 0 < question < 26:
                quiz(uid, username, question, answer)
                return
            LOGGER.error('COULDNT UNDERSTAND %s', text)
            BEBOT.send(uid, strings.BAD_REQUEST)
        except:
            LOGGER.error('COULDNT UNDERSTAND %s', text)
            BEBOT.send(uid, strings.BAD_REQUEST)
            return

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
        for msg in BEBOT.get(UPDATE_ID):
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
