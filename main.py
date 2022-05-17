from pyrogram import Client  # телеграм клиент
from pyrogram import filters
from pyrogram.types import (
	ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
import telebot
from telebot import types
import shelve
import re
import config
import datetime

############################

API_ID = config.API_ID
API_HASH = config.API_HASH
PRIVATE_PUBLIC = config.PRIVATE_PUBLIC
PUBLIC_PUBLIC = config.PUBLIC_PUBLIC
SOURCE_PUBLICS = config.SOURCE_PUBLICS
PHONE_NUMBER = config.PHONE_NUMBER

BOT_TOKEN = config.BOT_TOKEN

chanel_short_name_1 = ''
chanel_long_name_1 = '' 
chat_kuda_ID = -1 

chanel_short_name_2 = ''
chanel_long_name_2 = ''

chanel_short_name_3 = ''
chanel_long_name_3 = ''

############################

db = shelve.open('data.db', writeback=True)
app = Client("grabber", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)
bot = telebot.TeleBot(BOT_TOKEN)

##############################

def add_post_to_db(message):
	try:
		new_id = max(int(k) for k in db.keys()
					 if k.isdigit()) + 1
	except:
		new_id = 1

	db[str(new_id)] = {
		'username': message.chat.username,
		'message_id': message.id,
	}
	return new_id

##############################

@app.on_message(filters.chat(SOURCE_PUBLICS))
def new_channel_post(client, message):
	post_id = add_post_to_db(message)
	message.forward(PRIVATE_PUBLIC)
	client.send_message(PRIVATE_PUBLIC, post_id)



##############################

@app.on_message(filters.chat(PRIVATE_PUBLIC) & filters.regex(r'\d+\++\D{2,}') )
def post_request(client, message):
	stroka = message.text
	stroka_partition = stroka.partition('+')
	post_id = str(stroka_partition[0])
	stroka_part_2 = stroka_partition[2].partition('+')
	chanel_short_name = stroka_part_2[0]
	hashtag = stroka_part_2[2]


	post = db.get(post_id)

	if post is None:
		client.send_message(PRIVATE_PUBLIC, '`ERROR NO POST ID IN DB`')
		return

	try:
		msg = client.get_messages(post['username'], post['message_id'])

		if msg.text :
			msg_text = msg.text
		elif msg.caption :
			msg_text = msg.caption

		if chanel_short_name == chanel_short_name_1 :
			msg_text = msg_text + '\n\n' + hashtag

			############################
			buttons = [
				types.InlineKeyboardButton(text="кнопка 1", url="https://ya.ru"),
				types.InlineKeyboardButton(text="кнопка 1", url="https://ya.ru")
			]
			keyboard = types.InlineKeyboardMarkup(row_width=1)
			keyboard.add(*buttons)

			bot.send_message(chat_kuda_ID, msg_text, reply_markup=keyboard)
			client.send_message(PRIVATE_PUBLIC, f'`Успешно! SUCCESS REPOST!`')

			## КОНЕЦ fr ##########################


		elif chanel_short_name == chanel_short_name_2 :

			msg_text = msg_text + '\n\n' + hashtag

			client.send_message(chanel_long_name_2, msg_text, disable_web_page_preview=True, disable_notification=False)
			client.send_message(PRIVATE_PUBLIC, f'`Успешно! SUCCESS REPOST!`')

		elif chanel_short_name == chanel_short_name_3 :

			msg_text = msg_text + '\n\n' + hashtag

			client.send_message(chanel_long_name_3, msg_text, disable_web_page_preview=True, disable_notification=False)
			client.send_message(PRIVATE_PUBLIC, f'`Успешно! SUCCESS REPOST!`')

		else:
			client.send_message(PRIVATE_PUBLIC, f'`ОШИБКА! Канал задан неверно`')

	except Exception as e:
		client.send_message(PRIVATE_PUBLIC, f'`ERROR {e}`')



##########################################################
##########################################################
if __name__ == '__main__':
	now = datetime.datetime.now()
	now_ctr = now.strftime("%d.%m-%Y %H:%M")
	print('AA_si_graber.py запущен! - ' + now_ctr)
	app.run()  # эта строка запустит все обработчики