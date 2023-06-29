from environs import Env

# Теперь используем вместо библиотеки python-dotenv библиотеку environs
env = Env()
env.read_env()

BOT_TOKEN = env.str("BOT_TOKEN")  # Забираем значение типа str
ADMINS = env.list("ADMINS")  # Тут у нас будет список из админов

SUPABASE_URL = env.str("SUPABASE_URL")
SUPABASE_KEY = env.str("SUPABASE_KEY")

PAYMENT_TOKEN = env.str("PAYMENT_TOKEN")

BOT_NICKNAME = "SFS47_bot"

VIDEOS = {
    "android": "BAACAgIAAxkBAAIFymSQSpYPexBq0uEy-Oc3mPpdiouUAALKJAACXr14SibanVcYOyOrLwQ",
    "iphone": "BAACAgIAAxkBAAIFy2SQSrPW6PcabMG12XkioFN4Tb4bAALJJAACXr14SvwIY2evecuULwQ"
}

amounts = {
    1: 400,
    2: 800,
    3: 1200,
    4: 1500
}
