import os

# Application Name
APP_NAME = "QUIONGOSPI"

# API Parameters
API_HOST = "localhost"
API_PORT = 5000

# Debug
DEBUG = False

# Directories
HOME_DIR = os.path.join("/home", "pi", "Desktop", "quiongos", "pi")

# Datetime Formats
DATETIME = "%Y-%m-%d %H:%M:%S"
DATE = "%Y-%m-%d"

# Database Parameters
QUIONGA_DB = {"DB_NAME": "quionga",
              "DB_HOST": "localhost",
              "DB_PORT": "5432",
              "DB_USER": "pi",
              "DB_PASS": os.getenv("PI_PASS")}

ZOMIC_DB = {"DB_NAME": "zomic",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USER": "pi",
            "DB_PASS": os.getenv("PI_PASS")}

BEBOT_DB = {"DB_NAME": "bebot",
            "DB_HOST": "localhost",
            "DB_PORT": "5432",
            "DB_USER": "pi",
            "DB_PASS": os.getenv("PI_PASS")}

DSN = "dbname="    + QUIONGA_DB["DB_NAME"] + \
      " user="     + QUIONGA_DB["DB_USER"] + \
      " host="     + QUIONGA_DB["DB_HOST"] + \
      " password=" + QUIONGA_DB["DB_PASS"]

# Size Limits
TEXT = 5000 #Rule, Proposal, Tax Description
NAME = 200 #Name, Email
WALLET = 42
TXID = 66

# Telegram Bot
ZOMICBOT_TOKEN = os.getenv("ZOMICBOT_TOKEN")
BEBOT_TOKEN = os.getenv("BEBOT_TOKEN")
ZOMICBOT_URL = "https://api.telegram.org/bot{}".format(ZOMICBOT_TOKEN)
BEBOT_URL = "https://api.telegram.org/bot{}".format(BEBOT_TOKEN)
TELEGRAM_SLEEP = 2
TELEGRAM_OFFSET = 911210210

#################################################################################
#################################### GENESIS ####################################
#################################################################################
#Community Multi-Sig Wallet
MULTI_SIG = None

# Founders
GENESIS_MEMBERS = ["baraberto", "ritapg"]

# Initial Rules
RULE_1 = "Imposto semanal de 1 DAI por membro, a ser depositado na wallet %s."
RULE_2 = "Cada DAI investido reverte em um ponto para o respectivo membro"
RULE_3 = "Semanalmente, cada membro pode propor uma nova regra.\n" + \
         "Caso a proposta seja aprovada (upvotes>downvotes), o autor da " + \
         "proposta recebe X pontos (X=upvotes-downvotes).\n" + \
         "Se esta for concorrente de outra já existente necessita de " + \
         "maior aprovação que a anterior até um limite de 75%.\n" + \
         "Se duas propostas forem concorrentes, apenas a que conseguir " + \
         "maior aprovação prevalece."
RULE_4 = "Semanalmente, cada membro pode propor uma novo membro.\n" + \
         "Caso o membro seja aprovado (upvotes>downvotes), o autor da " + \
         "proposta recebe 1 ponto e o novo membro inicia funcões."
RULE_5 = "Um membro pode votar em qualquer votação, recebe 1 ponto por voto."
RULE_6 = "Semanalmente, é subtraído um ponto por cada DAI em dívida " + \
         "ao respectivo membro.\n" + \
         "Caso volte aos 0 pontos é removido da comunidade.\n" + \
         "Poderá reentrar caso seja aprovado após proposta de um membro."
GENESIS_RULES = [RULE_1 % MULTI_SIG, RULE_2, RULE_3, RULE_4, RULE_5, RULE_6]
