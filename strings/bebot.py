#GET UNICODE FOR ICONS https://apps.timwhitlock.info/unicode/inspect
DEFAULT_ROLE = ["/groom", "/bride"]
LAST_DAY_ROLE = ["/drunk"]
SWAPPABLE_ROLE = ["/missingFriend", "/luckyFriend"]
AUTO_ACCEPT_ROLE = ["/luckyFriend"]
NEED_TEAM_ROLE = ["/groomsSpy", "/bridesSpy", "/coyBoy", "/coyGirl"]

BAD_REQUEST = """
Don't know what to reply
Type /help to get your available options
"""

START = """
Help me set \U0001F525 to a wedding
/new wedding or /join wedding
/help for more options
"""

NEW = """
Wedding Planned
Check /guestlist
"""

ALREADY_NEW = """
Already planning a wedding
Check /guestlist or /delete wedding
"""

GUESTLIST = """
Invited: %d
Accepted: %d
/guestlist: %s
Room 0: %s
Room 1: %s
Invite more /guests
After everyone /join let's /party 
"""

WHICH_GUESTLIST = """
Which /guestlist do you want to check ? %s
"""

NO_WEDDING_PLANNED = """
You didn't plan any wedding
Plan a /new wedding
"""

ADDED = """
Guest %s added
Check /guestlist or invite more /guests
"""

REMOVED = """
Guest %s removed
Check /guestlist
"""

DELETED = """
Wedding deleted from your historic
"""

JOIN = """
Which wedding do you wish to /join ? %s
"""

JOINED = """
You joined the wedding
Current guestlist: %s
"""

LEAVE = """
I'm sorry that you can't make it to the wedding
If you change your mind /join again
"""

GUESTLIST_FULL = """
I'm sorry, I'm not accepting any more guests
"""

NO_WEDDING_AVAILABLE = """
There are no weddings available
Consider planning a /new one
"""

ALREADY_PARTYING = """
Party has already started
Type /help for more options
"""

CANT_PARTY = """
Can't party with less than 6 accepted /guests
The invitees have to /join the wedding
Check your /guestlist
"""

PARTY_DETAILS = """
Wedding /guestlist
Days: %d
Hostages: %s
Your starting room: %d
"""

INVALID_LAST = """
Bad request, use it on the /last day for:
- Wedding planner to warn %s
- %s to request to be warned
""" % (LAST_DAY_ROLE, LAST_DAY_ROLE)

LAST = """
It's the /last day?
Inform %s of his role
""" % LAST_DAY_ROLE

INVALID_SHARE = """
Bad request, you are not in any /guestlist
Consider /join or create a /new wedding
"""

SHARE_WITH = """
With whom do you wish to share ?%s
"""

INVALID_WITH = """
Bad Request, you don't have any /share
Or couldn't find the /guest with whom you want to share
"""

MUTUAL = """
He also has to share with you, /yes or /no ?
"""

INVALID_MUTUAL = """
Bad Request, you don't have any pending /share
"""

ACCEPT = """
You received a %s request
Do you /accept_%s or /reject_%s ?
"""

SHARED = """
You shared with %s
Check his sticker:
"""

REJECTED = """
Share rejected
"""

RECEIVED = """
You received info from %s
Check his sticker:
"""

GOT_SWAPPED = """
Your role has swapped
"""

NO_HOSTAGES = """
Bad Request, exchange hostages only after /party
"""

HOSTAGES = """
Choose the hostage to leave room%s
"""

HELP = """
Your available options are:
/start - Talk with the Groom Bot
/new - Plan a new wedding
/join - Join an existing wedding
/guestlist - Check wedding details
/delete - Delete planned wedding
/party - Party time
/guests - Guest options
/guests_groom - /groom guest options
/guests_bride - /bride guest options
/guests_neutral - Neutral guest options
/guests_short - No /guests details
/share_role - Share your role
/share_team - Share your team
/hostages - Exchange hostages
/last - Warn %s about his role
/template - Check wedding templates
/rules - Wedding rules
/help - Help from the Groom Bot
""" % LAST_DAY_ROLE
#/guests_name - Real /guests name
#/yes - Share has to be mutual
#/no - No need to share back
#/accept - Accept a share request
#/reject - Reject a share request

RULES = """
You have the wedding /guests evenly split between two rooms
Each day some /guests will be held hostage and forced to exchange rooms
In the last day if /groom and /bride end up in the same room they get married

/guests_groom want to avoid this marriage
/guests_bride want to consummate this marriage
/guests_neutral have their own agenda \U0001F37B

You don't know anything about anybody else
You have to argue and decide who should be held hostage each day
You may show your role privately or openly
"""

START_STICKER = "CAADBAADLAADTwqNIF1JUDA50bmWAg"
TEAM_BE_STICKER = "CAADBAADLQADTwqNIFiTkkrX8G1UAg"
TEAM_CAROL_STICKER = "CAADBAADLgADTwqNIP80XW-iEx5PAg"
NO_TEAM_STICKER = "CAADBAADLwADTwqNICmSfGrOQcpVAg"
LULA_TEAM_STICKER = "CAADBAADMAADTwqNIFmB_vfNkQP6Ag"

CHARACTERS = {
    "/groom": {
        "name": "Bé",
        "with": ["/bride"],
        "goal": "Avoid getting married",
        "sticker": "CAADBAADMQADTwqNIMK7uUKzQdHTAg",
        "team": TEAM_BE_STICKER},
    "/bride": {
        "name": "Carol",
        "with": ["/groom"],
        "goal": "Marry /groom",
        "sticker": "CAADBAADMgADTwqNIIRsBykQ8ChdAg",
        "team": TEAM_CAROL_STICKER},
    "/bestMan": {
        "name": "Chico Pinto",
        "with": ["/bridesmaid"],
        "goal": "Meet /groom before the wedding day",
        "sticker": "CAADBAADMwADTwqNIBMAAZovCyFTHAI",
        "team": TEAM_BE_STICKER},
    "/bridesmaid": {
        "name": "Maria Inês",
        "with": ["/bestMan"],
        "goal": "Meet /bride before the wedding day",
        "sticker": "CAADBAADNAADTwqNIKb7DxM6aAmDAg",
        "team": TEAM_CAROL_STICKER},
    "/groomBot": {
        "name": "Bé Bot",
        "with": ["/brideDouble"],
        "goal": "Avoid getting married if /groom is not in play",
        "sticker": "CAADBAADNQADTwqNIHw9iBplkv3fAg",
        "team": TEAM_BE_STICKER},
    "/brideDouble": {
        "name": "Sósia Carol",
        "with": ["/groomBot"],
        "goal": "Marry /groom if /bride is not in play",
        "sticker": "CAADBAADNgADTwqNII3uzvJGGSCYAg",
        "team": TEAM_CAROL_STICKER},
    "/2ndBestMan": {
        "name": "Caldeira",
        "with": ["/bestMan", "/bridesmaid", "/2ndBridesmaid"],
        "goal": "Meet /groom before the wedding day if /bestMan is not in play",
        "sticker": "CAADBAADNwADTwqNIGOdRAZZPz2HAg",
        "team": TEAM_BE_STICKER},
    "/2ndBridesmaid": {
        "name": "Caru",
        "with": ["/bridesmaid", "/bestMan", "/2ndBestMan"],
        "goal": "Meet /bride before the wedding day if /bridesmaid is not in play",
        "sticker": "CAADBAADOAADTwqNIOEL-2kHmCIVAg",
        "team": TEAM_CAROL_STICKER},
    "/bridesSpy": {
        "name": "Tiago Fonseca",
        "with": ["/groomsSpy", "/coyBoy", "/coyGirl"],
        "goal": "You are a SPY! Make sure there is a wedding",
        "sticker": "CAADBAADOQADTwqNIO5PswriE8IhAg",
        "team": TEAM_BE_STICKER},
    "/groomsSpy": {
        "name": "Cátia Lopo",
        "with": ["/bridesSpy", "/coyBoy", "/coyGirl"],
        "goal": "You are a SPY! Make sure there is NO wedding",
        "sticker": "CAADBAADOgADTwqNINUaz76uqq9hAg",
        "team": TEAM_CAROL_STICKER},
    "/coyBoy": {
        "name": "José Vicente",
        "with": ["/bridesSpy", "/groomsSpy", "/coyGirl"],
        "goal": "You are a COY! You can NOT show your role, only your team",
        "sticker": "CAADBAADOwADTwqNIIVSdjLdKOiGAg",
        "team": TEAM_BE_STICKER},
    "/coyGirl": {
        "name": "Mariana Freire",
        "with": ["/bridesSpy", "/groomsSpy", "/coyBoy"],
        "goal": "You are a COY! You can NOT show your role, only your team",
        "sticker": "CAADBAADPAADTwqNIKbd1Epmlqc6Ag",
        "team": TEAM_CAROL_STICKER},
    "/groomsRebel": {
        "name": "Avó Maria Teresa",
        "with": ["/bridesRebel"],
        "goal": "You may usurp the room leadership once by publicly revealing your card",
        "sticker": "CAADBAADPQADTwqNILrCv90gndtAAg",
        "team": TEAM_BE_STICKER},
    "/bridesRebel": {
        "name": "Antónia Peças",
        "with": ["/groomsRebel"],
        "goal": "You may usurp the room leadership once by publicly revealing your card",
        "sticker": "CAADBAADPgADTwqNINY2NIdgS8u1Ag",
        "team": TEAM_CAROL_STICKER},
    "/groomsBodyguard": {
        "name": "Cyborg",
        "with": ["/bridesBodyguard"],
        "goal": "You may force someone to stay once by publicly revealing your card",
        "sticker": "CAADBAADPwADTwqNILKgpHiY01nyAg",
        "team": TEAM_BE_STICKER},
    "/bridesBodyguard": {
        "name": "Maria Batalha",
        "with": ["/groomsBodyguard"],
        "goal": "You may force someone to stay once by publicly revealing your card",
        "sticker": "CAADBAADQAADTwqNIF_GP94xxLwgAg",
        "team": TEAM_CAROL_STICKER},
    "/shyGuy": {
        "name": "Luís Barros",
        "with": ["/shyGirl"],
        "goal": "You are shy, you may NEVER reveal your card or team to anyone",
        "sticker": "CAADBAADQQADTwqNIA3nuZvGmuW7Ag",
        "team": TEAM_BE_STICKER},
    "/shyGirl": {
        "name": "Clara Vicente",
        "with": ["/shyGuy"],
        "goal": "You are shy, you may NEVER reveal your card or team to anyone",
        "sticker": "CAADBAADQgADTwqNIOSw7xTWCFanAg",
        "team": TEAM_CAROL_STICKER},
    "/groomsParanoid": {
        "name": "Casinhas",
        "with": ["/bridesParanoid"],
        "goal": "You are paranoid, you may only reveal your card ONCE",
        "sticker": "CAADBAADQwADTwqNICMm7QifMbFWAg",
        "team": TEAM_BE_STICKER},
    "/bridesParanoid": {
        "name": "Estelle",
        "with": ["/groomsParanoid"],
        "goal": "You are paranoid, you may only reveal your card ONCE",
        "sticker": "CAADBAADRAADTwqNINwXtYd9A4qSAg",
        "team": TEAM_CAROL_STICKER},
    "/groomsGuest": {
        "name": "Luís Rodrigues",
        "with": ["/bridesGuest"],
        "goal": "Help /groom avoiding his marriage",
        "sticker": "CAADBAADRQADTwqNIIuKCL0zZrHDAg",
        "team": TEAM_BE_STICKER},
    "/bridesGuest": {
        "name": "Carolina Sousa",
        "with": ["/groomsGuest"],
        "goal": "Help /bride marrying /groom",
        "sticker": "CAADBAADRgADTwqNIB8IhufTidHsAg",
        "team": TEAM_CAROL_STICKER},
    "/missingFriend": {
        "name": "Ana Rocha",
        "with": [],
        "goal": "You LOSE! But, if you card share with someone discretely /swap cards",
        "sticker": "CAADBAADRwADTwqNIMMyNAvyGHLtAg",
        "team": NO_TEAM_STICKER},
    "/luckyFriend": {
        "name": "Zequinha",
        "with": [],
        "goal": "You WIN! But, if someone asks to card share with you discretely /swap cards",
        "sticker": "CAADBAADSAADTwqNIDXQ1E5XY-xVAg",
        "team": NO_TEAM_STICKER},
    "/priest": {
        "name": "Padre",
        "with": [],
        "goal": "Meet both /groom and /bride before the wedding day",
        "sticker": "CAADBAADSQADTwqNIGnlJXuexMo1Ag",
        "team": NO_TEAM_STICKER},
    "/knowItAll": {
        "name": "Rita Gomes",
        "with": [],
        "goal": "On the wedding day, guess if there is going to be a wedding or not",
        "sticker": "CAADBAADSgADTwqNIH-W0uyp8IOfAg",
        "team": NO_TEAM_STICKER},
    "/drunk": {
        "name": "Lula",
        "with": [],
        "goal": "You may only pick your 'real' card on the day before the wedding",
        "sticker": "CAADBAADSwADTwqNIAxcno61R70aAg",
        "team": LULA_TEAM_STICKER},
    "/familysDog": {
        "name": "Belchior",
        "with": [],
        "goal": "Be sure the first person that card shared with you wins",
        "sticker": "CAADBAADTAADTwqNIEe0zksLNCu2Ag",
        "team": NO_TEAM_STICKER},
    "/familysCat": {
        "name": "Cenoura",
        "with": [],
        "goal": "Be sure the first person that card shared with you loses",
        "sticker": "CAADBAADTQADTwqNIG7TF33xO4cnAg",
        "team": NO_TEAM_STICKER},
    "/traveller": {
        "name": "Marçal",
        "with": [],
        "goal": "Be sure to exchange rooms on most of the rounds",
        "sticker": "CAADBAADTgADTwqNICROl0TB0BtUAg",
        "team": NO_TEAM_STICKER},
    "/onDuty": {
        "name": "Dona Nanda",
        "with": [],
        "goal": "Be sure to stay in your room during all rounds",
        "sticker": "CAADBAADTwADTwqNIKpOl1hjFd7sAg",
        "team": NO_TEAM_STICKER},
    "/groomsBrother": {
        "name": "Tiago Barros",
        "with": ["/bridesSister"],
        "goal": "Be with /groom at the wedding day",
        "sticker": "CAADBAADUAADTwqNIIrcQKPazbNyAg",
        "team": NO_TEAM_STICKER},
    "/bridesSister": {
        "name": "Joana Santos",
        "with": ["/groomsBrother"],
        "goal": "Be with /bride at the wedding day",
        "sticker": "CAADBAADUQADTwqNIGi1Kqa9kRBeAg",
        "team": NO_TEAM_STICKER},
    "/juliet": {
        "name": "Leonor Catita",
        "with": ["/romeo"],
        "goal": "Be with /romeo and /bride at the wedding day",
        "sticker": "CAADBAADUgADTwqNIIH5mkq9km_FAg",
        "team": NO_TEAM_STICKER},
    "/romeo": {
        "name": "Rúben Franco",
        "with": ["/juliet"],
        "goal": "Be with /juliet and /bride at the wedding day",
        "sticker": "CAADBAADUwADTwqNIKGBj7QZR5ObAg",
        "team": NO_TEAM_STICKER},
}

TEMPLATES = {
    "/template_coldWar": {
        "roles": ["/groom", "/bride",
                  "/bestMan", "/bridesmaid",
                  "/bridesSpy", "/groomsSpy", "/coyBoy", "/coyGirl",
                  "/shyGuy", "/shyGirl"],
        "invites": 10
    },
    "/template_shyGuy": {
        "roles": ["/groom", "/bride",
                  "/bestMan", "/bridesmaid",
                  "/shyGuy", "/shyGirl",
                  "/groomsParanoid", "/bridesParanoid",
                  "/groomsGuest", "/bridesGuest"],
        "invites": 10
    },
    "/template_royalRumble": {
        "roles": ["/groom", "/bride",
                  "/bestMan", "/bridesmaid",
                  "/missingFriend", "/luckyFriend",
                  "/priest", "/knowItAll",
                  "/familysDog", "/familysCat"],
        "invites": 10
    },
}
