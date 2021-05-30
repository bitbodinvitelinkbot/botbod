from telegram import * 
from telegram.ext import *
from config import *
from openpyxl import load_workbook
from pathlib import Path
from texts import texts
import os, shutil



# initial variables
u = Updater(BOT_TOKEN)
d = u.dispatcher
bot = Bot(BOT_TOKEN)
EXCEL_FILE = str(Path(os.path.realpath(__file__)).parent / EXCEL_FILE)


def check(inp):
    inp = str(int(inp))
    if inp.startswith('98'):
        inp = inp[2:]
    elif inp.startswith('+98'):
        inp = inp[3:]
    if len(inp) != 10:
        return False

    workbook = load_workbook(EXCEL_FILE)
    sheet = workbook.active
    def list_values(col):
        return map(lambda item: str(item.value), sheet[col])
    database = dict(zip(list_values('A'), list_values('B')))

    return database.get('0' + inp)

def all_handler(update, context):
    message = update.message
    if message:
        contact = message.contact
        if contact.user_id == message.to_dict()['from']['id']:
            output = check(int(contact.phone_number))
            if output == False:
                message.reply_text(texts['wrong-number'])
            elif output == None:
                message.reply_text(texts['not-found'])
            else:
                message.reply_text(output)
        else:
            message.reply_text(texts['your-own-contact'])


def help_handler(update, context):
    message = update.message
    if message:
        message.reply_text(texts['tutorial'])

def other_messages(update, context):
    message = update.message
    if message:
        message.reply_text(texts['not-recognized'])


for handler in [
    CommandHandler('start', help_handler),
    CommandHandler('help', help_handler),
    
    MessageHandler(Filters.contact, all_handler),

    MessageHandler(Filters.all, other_messages),
]:
    d.add_handler(handler)


# polling
u.start_polling()
print('polling...')
u.idle()