import settings
import requests

def bot_sendtext(bot_message):
    
	
	# Send text message
	bot_token = settings.notification_bot_token
	bot_chatID = settings.admin1      # chat IDs of users you want to send message to
	send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
 
	requests.get(send_text)
    

bot_sendtext("ducks")