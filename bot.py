import logging
from telegram import Update, ForceReply
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import jwt
import requests
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
JWKS_URL = os.get('JWKS_URL')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_html(
        rf'Hi {user.mention_html()}!',
        reply_markup=ForceReply(selective=True),
    )

def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('Help!')


def create_jwt(user_details):
    payload = {
        'user_id': user_details['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm='RS256')
    return token

def verify_jwt(token):
    jwks_url = JWKS_URL  
    response = requests.get(jwks_url)
    jwks = response.json()
    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(jwks['keys'][0])
    decoded = jwt.decode(token, public_key, algorithms=['RS256'])
    return decoded

async def handle_message(update: Update, context: CallbackContext) -> None:
    user_details['id'] = update.message.from_user_id
    jwt_token = create_jwt(user_details)
    update.message.reply_text(f'JWT Token: {jwt_token}')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("login", login))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
