from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")
# API_ID = env.str("API_ID")
# API_HASH = env.str("API_HASH")
#
# SESSION_NAME = env.str("SESSION_NAME")

MYSQL_HOST = env.str("MYSQL_HOST")
MYSQL_USER = env.str("MYSQL_USER")
MYSQL_PASS = env.str("MYSQL_PASS")
