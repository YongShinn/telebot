# -*- coding: utf-8 -*-
# 788731481:AAF30CxdR5WM5uZGTCKzAAzpySlTTPZN4CY
# 756019399:AAHQ7u2zq_JHdf_bODDdwRUOFeW923qRquo

import time
import database

import telebot
from telebot import types
import scrape
from threading import Thread

TOKEN = '756019399:AAHQ7u2zq_JHdf_bODDdwRUOFeW923qRquo'

bubbletype = 'asd'

finalMsg = """Final shopping cart:\n"""

Customeritem = ['username', 'brand', 'link', 'qty',
                'size', 'color', 'location', 'Prod_name', 1.1, 1.1]
# Store username, retailer, link, quantity, size, color, location, produce_name, total price, unit price respectively
# Used for creating of cart

Joinitem = ['UCN', 'link1', 'qty1', 'size1',
            'color1', 'Prod_name', 1.1, 'name', 1.1]
# Store UCD, link, quantity, size, color, produce_name, total price, ChatID, unit price respectively
#Used for join

Edititem = ['PTN', 'first_name', [], 'choice', 'properties', 'changes']
# Store PTN, username, List of itemName & itemID, choice, properties, changes
# Used in edit

Backend_stuff = [1, 1, 1, '1', 1, '1', 1]
# Store userID, retailerID, bubbleID, UCD, itemID, PTN, timer respectively
# Used to store what was retrieve from the Backend

commands = {  # Initialisation of Command
    'start': 'Welcome to Buyn',
    'create': 'Create new CART',
    'join': 'Join an existing CART',
    'edit': 'Edit order',
    'faq': 'Frequently Asked Question',
    'help': 'help',
    'recommendbrand': 'Recommend us some brands!',
    'brandlist': 'View current brands on Buyn',
    'return': 'Return',
}


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print(str(m.chat.first_name) +
                  " [" + str(m.chat.id) + "]: " + m.text)


bot = telebot.TeleBot(TOKEN)
bot.set_update_listener(listener)  # register listener


# handle the "/start" command
# Creation of Home's menu and Button
@bot.message_handler(commands=['start'])
def command_start(m):
    cid = m.chat.id
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/create')
    itembtn2 = types.KeyboardButton('/join')
    itembtn3 = types.KeyboardButton('/edit')
    itembtn4 = types.KeyboardButton('/help')
    itembtn5 = types.KeyboardButton('/brandlist')
    itembtn6 = types.KeyboardButton('/recommendbrand')
    itembtn7 = types.KeyboardButton('/statue')
    itembtn8 = types.KeyboardButton('/faq')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4,
               itembtn5, itembtn6, itembtn7, itembtn8)
    bot.send_message(cid, "Welcome to Buyn", reply_markup=markup)


# handle the "/create" command
# creating Retailer buttons
@bot.message_handler(commands=['create'])
def command_create(m):
    cid = m.chat.id
    Customeritem[0] = cid
    print(Customeritem[0])
    bot.send_chat_action(cid, 'typing') 
    markup2 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Colorpop: [$50]💄')
    itembtn2 = types.KeyboardButton('Sephora: [$40]💄')
    itembtn3 = types.KeyboardButton('Sephora: [$110]💄')
    itembtn4 = types.KeyboardButton('Uniqlo: [$60]👚')
    itembtn5 = types.KeyboardButton('Zara: [$79]👚')
    itembtn6 = types.KeyboardButton("The Editor's Market: [$60]👚")
    itembtn7 = types.KeyboardButton("The Editor's Market: [$60]👚")
    itembtn8 = types.KeyboardButton('The Tinsel Rack: [$100]👚')
    itembtn9 = types.KeyboardButton('Abercrombie & Fitch: [$160]👚')
    itembtn10 = types.KeyboardButton('Gardenpicks: [$50]🥜')
    itembtn11 = types.KeyboardButton('MyProtein: [$100]💊')
    markup2.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5,
                itembtn6, itembtn7, itembtn8, itembtn9, itembtn10, itembtn11)
    msg = bot.reply_to(m, """Hello there! 😊 Seems like you’re creating a new cart to share.

This is a list of all minimum basket size to qualify for free shipping by retailers. Take a look!:

Colorpop: $50 💄 https://colourpop.com/

Sephora: $40 [FREE SHIPPING] $110 [FREE NEXT DAY] 💄 https://www.sephora.sg/

Uniqlo: $60 👚 https://www.uniqlo.com/sg/store/#undefined

Zara: $79 👚 https://www.zara.com/sg/ 

The Editor’s Market: Free Shipping, discount starts at 3 pieces and more, discounts up to 6 pieces. We are offering two options for you at $60 and $120 👚 https://www.theeditorsmarket.com/

The Tinsel Rack: $100 👚 https://www.thetinselrack.com/

Abercrombie & Fitch: $160 👚 https://www.abercrombie.sg/en_SG/home

Gardenpicks: $50 🥜 http://gardenpicks.com.sg/

MyProtein: $100 💊 http://gardenpicks.com.sg/

Can you please give us the name of the brand that you will be shopping from? 📥""", reply_markup=markup2)
    bot.register_next_step_handler(msg, create_chooseBrand) # display msg and jumping to next function

# firstly if its the first time
# else store retailer option and asking for link
def create_chooseBrand(message):
    try:
        if (message == Customeritem[1]):
            print("asd")
            msg = bot.send_message(Customeritem[0], """Send Link1""")
            bot.register_next_step_handler(msg, create_screenshot)
        else:
            chat_id = message.chat.id
            Customeritem[1] = message.text
            print(Customeritem[1])
            Backend_stuff[2] = scrape.checkRetail(Customeritem[1])
            print(Backend_stuff[2])
            markup3 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Cancel')
            markup3.add(itembtn1)
            msg = bot.reply_to(message, """Send Link""", reply_markup=markup3)
            bot.register_next_step_handler(msg, create_screenshot) # display msg and jumping to next function
    except Exception as e:
        bot.reply_to(message, 'oooops')

#            #
# SCREENSHOT #
#            # 
# Check if the user previously try to cancel
# Ask for quantity
def create_screenshot(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            link1 = message.text
            Customeritem[2] = link1
            print(Customeritem[2])
            markup5 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('1')
            itembtn2 = types.KeyboardButton('2')
            itembtn3 = types.KeyboardButton('3')
            itembtn4 = types.KeyboardButton('Cancel')
            markup5.add(itembtn1, itembtn2, itembtn3, itembtn4)
            msg = bot.reply_to(message, """Qty?\nFor more, please type it out""", reply_markup=markup5)
            bot.register_next_step_handler(msg, create_screenshot_qty) # display msg and jumping to next function
    except Exception as e:
        bot.reply_to(message, 'oooops')
#           #
# QUANTITY  #
#           #
# Check if the user previously try to cancel
# Ask for Size
def create_screenshot_qty(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            qty1 = message.text
            Customeritem[3] = qty1
            print(Customeritem[3])
            markup6 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('XS')
            itembtn2 = types.KeyboardButton('S')
            itembtn3 = types.KeyboardButton('M')
            itembtn4 = types.KeyboardButton('L')
            itembtn5 = types.KeyboardButton('XL')
            itembtn6 = types.KeyboardButton('Cancel')
            markup6.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
            msg = bot.reply_to(message, """Size?\n(Please type out the your size if it's not available in the button)""", reply_markup=markup6)
            bot.register_next_step_handler(msg, create_screenshot_Size) # display msg and jumping to next function
    except Exception as e:
        bot.reply_to(message, 'oooops')

#           #
#   SIZE    #
#           #
# Check if the user previously try to cancel
# Ask for Color
def create_screenshot_Size(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            size1 = message.text
            Customeritem[4] = size1
            print(Customeritem[4])
            msg = bot.reply_to(message, """Color?\n(NA if not applicable)""")
            bot.register_next_step_handler(msg, create_screenshot_Color) # display msg and jumping to next function
    except Exception as e:
        bot.reply_to(message, 'oooops')

#           #
#   COLOR   #
#           #
# Check if the user previously try to cancel
# Display confirmation
def create_screenshot_Color(message):
    try:
        chat_id = message.chat.id
        color1 = message.text
        Customeritem[5] = color1
        print(Customeritem[5])
        markup7 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Yes')
        itembtn2 = types.KeyboardButton('No')
        markup7.add(itembtn1, itembtn2)
        Customeritem[7] = scrape.scraping(
            Customeritem[1], Customeritem[2], Customeritem[3])[0] # scraping for prodName
        print(Customeritem[7])
        Customeritem[9] = float(scrape.scraping(
            Customeritem[1], Customeritem[2], Customeritem[3])[1]) #scraping for unitPrice
        Customeritem[8] = float(scrape.scraping(
            Customeritem[1], Customeritem[2], Customeritem[3])[1]) * float(Customeritem[3]) # Multiplication for totalPrice
        msg = bot.reply_to(message, """Title: """ + Customeritem[7] + '\nPrice: $' + str(Customeritem[8]) + '\nQty: ' + Customeritem[3] +
                           '\nSize: ' + Customeritem[4] + '\nColor: ' + Customeritem[5] + "\nDo you want to confirm this order?", reply_markup=markup7)
        global finalMsg
        finalMsg = finalMsg + """Title: """ + Customeritem[7] + '\nPrice: $' + str(Customeritem[8]) + '\nQty: ' + Customeritem[3] + '\nSize: ' + Customeritem[4] + '\nColor: ' + Customeritem[5] + "\n\n"
        bot.register_next_step_handler(msg, create_bubbletype) # display msg and jumping to next function
    except Exception as e:
        bot.reply_to(message, 'oooops')
#              #
# Confirmation #
#              #
# Check if the user previously try to cancel
# Display location
def create_bubbletype(message):
    try:
        chat_id = message.chat.id
        confirmation = message.text
        if (Backend_stuff[6] == 1): # checking if bubbleID is created else dont generate another bubbleID
            if (confirmation == 'Yes'):
                markup8 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
                itembtn1 = types.KeyboardButton('Public')
                itembtn2 = types.KeyboardButton('Private')
                markup8.add(itembtn1, itembtn2)
                msg = bot.reply_to(message, """Would like this cart to be private or public""", reply_markup=markup8)
                bot.register_next_step_handler(msg, create_confirm) # display msg and jumping to next function
            else:
                Thread(target=command_start(message)).start()
        else:
            Thread(target=create_location(message)).start()

    except Exception as e:
        msg = bot.reply_to(message, """""", reply_markup=markup8)
        bot.reply_to(msg, 'oooops')


#              #
# Bubble_type  #
#              #
# Check if the user previously try to cancel
# Display location
def create_confirm(message):
    try:
        chat_id = message.chat.id
        global bubbletype
        bubbletype = message.text
        if (bubbletype == 'Public'):
            markup7 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('UTown')
            itembtn2 = types.KeyboardButton('CLB')
            markup7.add(itembtn1, itembtn2)
            msg = bot.reply_to(message, """Aweasome, can we know where you want your items delivered to? 
Utown: Delivery will be done to cheers 
CLB: Central Library""", reply_markup=markup7)
            bot.register_next_step_handler(msg, create_location) # display msg and jumping to next function
        elif (bubbletype == 'Private'):
            msg = bot.reply_to(message, "Aweasome, can we know where you want your items deliverd to?")
            bot.register_next_step_handler(msg, create_location)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#          #
# Location #
#          #
# Check if the user previously try to cancel
# Asking for continue shopping
def create_location(message):
    try:
        if (Backend_stuff[6] == 1): # checking if bubbleID is created else dont generate another bubbleID
            chat_id = message.chat.id
            location = message.text
            Customeritem[6] = location
            print(Customeritem[6])
            Backend_stuff[0] = database.add_user(chat_id, message.chat.username, message.chat.first_name) # adding username to backend
            print(Backend_stuff[0])
            Backend_stuff[6] = Backend_stuff[6] + 1
            print(Backend_stuff[6])
            Backend_stuff[2], Backend_stuff[3] = database.add_bubble(
                Backend_stuff[1], Backend_stuff[0], bubbletype)
            print(Backend_stuff[2])
        Backend_stuff[4] = database.add_item(
            Backend_stuff[1], Customeritem[2], Customeritem[7], Customeritem[9], Customeritem[4], Customeritem[5], int(Customeritem[3])) # adding item into backend and itemID
        print(Backend_stuff[4])
        Backend_stuff[5] = database.add_order(
            Backend_stuff[2], Backend_stuff[0], Backend_stuff[4], Customeritem[6]) # adding order and get PTN
        print(Backend_stuff[5])
        markup9 = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('Yes')
        itembtn2 = types.KeyboardButton('No')
        markup9.add(itembtn1, itembtn2)
        msg = bot.reply_to(
            message, """Do you want to continue shopping with the same retailer?""", reply_markup=markup9)
        bot.register_next_step_handler(msg, create_continue)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#          #
# continue #
#          #
# Checking if need to continue else display UCD and PTN
def create_continue(message):
    try:
        chat_id = message.chat.id
        c0ntinue = message.text
        print(c0ntinue)
        global finalMsg
        if(c0ntinue == 'Yes'):
            print("qwe")
            Thread(target=create_chooseBrand(Customeritem[1])).start()
        else:
            if (database.replace_ptn(Backend_stuff[5], Backend_stuff[2], Backend_stuff[0])):
                bot.send_message(chat_id, finalMsg)
                bot.send_message(chat_id, """Good choice!\nThis is your Personal Transaction Number (PTN) (do not share this!): """+Backend_stuff[5]+"""\nWe will ask for payments once your Cart is full!""")
                Backend_stuff[6] = 1
                bot.send_message(chat_id, """This is your Unique Cart Number (UCN): """+Backend_stuff[3]+"""\nFor now, get your friends to join your Cart! :-)""")
                finalMsg = """Final shopping cart:\n"""
                Thread(target=command_start(message)).start()
            else:
                bot.send_message(
                    chat_id, "Due to some technical issues, your purchase(s) wasn't store properly.\nPlease try again later.")
                Backend_stuff[6] = 1
                finalMsg = """Final shopping cart:\n"""
                Thread(target=command_start(message)).start()
    except Exception as e:
        bot.reply_to(message, 'oooops')
# Give username (add_user) take userID
# create bubble take bubble id and UCD
# After choosing brand, take retailer ID
# Add_item(overall_item) take item id
# add order() take PTN
# Replace all PTN relating to that user

# handle the "/join" command
# asking for UCN
@bot.message_handler(commands=['join'])
def command_join(m):
    cid = m.chat.id
    Joinitem[7] = cid
    bot.send_chat_action(cid, 'typing') 
    msg = bot.reply_to(
        m, """Hello there good looking 🤩, seems likes you’re joining a cart. Can we have the Unique Cart Number (UCN) please?""")
    bot.register_next_step_handler(msg, join_CartID)

#compare UCD to check if its the first time
#if first timer, ignore cariD and ask for link
#else store cartId and ask for link
def join_CartID(message):
    try:

        if (message == Joinitem[0]):
            print('asd')
            msg = bot.send_message(Joinitem[7], """Nice, please send over the link of your desired product! (Up to 3 pieces) 🛍🛍🛍

Remember to press 'Done' once you're ready!
""")
            bot.register_next_step_handler(msg, join_link)
        else:
            chat_id = message.chat.id
            CartID = message.text
            Joinitem[0] = CartID
            print(CartID)
            markup10 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Cancel')
            markup10.add(itembtn1)
            msg = bot.reply_to(message, """Nice, please send over the link of your desired product! 🛍🛍🛍

Remember to press 'Done' once you're ready!
""", reply_markup=markup10)
            bot.register_next_step_handler(msg, join_link)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#store link and ask for qty
def join_link(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            link1 = message.text
            print(link1)
            Joinitem[1] = link1
            markup11 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('1')
            itembtn2 = types.KeyboardButton('2')
            itembtn3 = types.KeyboardButton('3')
            itembtn4 = types.KeyboardButton('Cancel')
            markup11.add(itembtn1, itembtn2, itembtn3, itembtn4)
            msg = bot.reply_to(message, """Qty?\n(For more, please type it out)""", reply_markup=markup11)
            bot.register_next_step_handler(msg, join_qty)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#store qty and ask for size
def join_qty(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            qty1 = message.text
            print(qty1)
            Joinitem[2] = qty1
            markup12 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('XS')
            itembtn2 = types.KeyboardButton('S')
            itembtn3 = types.KeyboardButton('M')
            itembtn4 = types.KeyboardButton('L')
            itembtn5 = types.KeyboardButton('XL')
            itembtn6 = types.KeyboardButton('Cancel')
            markup12.add(itembtn1, itembtn2, itembtn3,
                         itembtn4, itembtn5, itembtn6)
            msg = bot.reply_to(message, """Size?\n(Please type out the your size if it's not available in the button)""", reply_markup=markup12)
            bot.register_next_step_handler(msg, join_size)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#Store size and ask for color
def join_size(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            size1 = message.text
            print(size1)
            Joinitem[3] = size1
            markup13 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Cancel')
            markup13.add(itembtn1)
            msg = bot.reply_to(message, """Color?\n(NA if not applicable)""", reply_markup=markup13)
            bot.register_next_step_handler(msg, join_color)
    except Exception as e:
        bot.reply_to(message, 'oooops')

#store color and display confirmation
def join_color(message):
    try:
        chat_id = message.chat.id
        if message.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            color1 = message.text
            print(color1)
            Joinitem[4] = color1
            Joinitem[5] = scrape.scraping(
                (Joinitem[0])[:3], Joinitem[1], Joinitem[2])[0]
            print(Joinitem[5])
            Joinitem[8] = float(scrape.scraping(
                (Joinitem[0])[:3], Joinitem[1], Joinitem[2])[1])
            Joinitem[6] = float(scrape.scraping(
                (Joinitem[0])[:3], Joinitem[1], Joinitem[2])[1]) * float(Joinitem[2])
            markup14 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Yes')
            itembtn2 = types.KeyboardButton('No')
            markup14.add(itembtn1, itembtn2)
            msg = bot.reply_to(message, """Title: """ + Joinitem[5] + '\nPrice: $' + str(Joinitem[6]) + '\nQty: ' + Joinitem[2] +
                               '\nSize: ' + Joinitem[3] + '\nColor: ' + Joinitem[4] + "\nDo you want to confirm this order?", reply_markup=markup14)
            global finalMsg 
            finalMsg = finalMsg + """Title: """ + Joinitem[5] + '\nPrice: $' + str(Joinitem[6]) + '\nQty: ' + Joinitem[2] + '\nSize: ' + Joinitem[3] + '\nColor: ' + Joinitem[4] + '\n\n'
            bot.register_next_step_handler(msg, join_confirm)
    except Exception as e:
        bot.reply_to(message, 'oooops')

# check confirmation and store all required ID
def join_confirm(message):
    try:
        chat_id = message.chat.id
        confirmation = message.text
        if (confirmation == 'Yes'):
            Backend_stuff[0] = database.add_user(chat_id, message.chat.username, message.chat.first_name)
            print(Backend_stuff[0])
            Backend_stuff[2], Backend_stuff[1] = database.retrieve_bubble(
                Joinitem[0])
            print(Backend_stuff[2])
            Backend_stuff[4] = database.add_item(
                Backend_stuff[1], Joinitem[1], Joinitem[5], Joinitem[8], Joinitem[3], Joinitem[4], int(Joinitem[2]))
            print(Backend_stuff[4])
            Backend_stuff[5] = database.add_order(
                Backend_stuff[2], Backend_stuff[0], Backend_stuff[4], (Joinitem[0])[7:])
            print(Backend_stuff[5])
            markup15 = types.ReplyKeyboardMarkup(
                row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Yes')
            itembtn2 = types.KeyboardButton('No')
            markup15.add(itembtn1, itembtn2)
            msg = bot.reply_to(
                message, """Do you want to continue shopping with the same retailer?""", reply_markup=markup15)
            bot.register_next_step_handler(msg, join_continue)
        else:
            Thread(target=command_start(message)).start()

    except Exception as e:
        bot.reply_to(message, 'oooops')

# check continue and display PTN UCD
def join_continue(message):
    try:
        chat_id = message.chat.id
        c0ntinue = message.text
        print(c0ntinue)
        global finalMsg
        if(c0ntinue == 'Yes'):
            print("qwe")
            Thread(target=join_CartID(Joinitem[0])).start()
        else:
            Thread(target=command_start(message)).start()
            if (database.replace_ptn(Backend_stuff[5], Backend_stuff[2], Backend_stuff[0])):
                bot.send_message(chat_id, finalMsg)
                bot.send_message(chat_id, """Good choice!\n""" 
+"""This is your Personal Transaction Number (PTN) (do not share this!): """+Backend_stuff[5]+"""\nWe will ask for payments once your Cart is full!""")
                bot.send_message(chat_id, """This is your Unique Cart Number (UCN): """+Joinitem[0]+"""For now, get your friends to join your Cart! :-)""")
                finalMsg = """Final shopping cart:\n"""
                Thread(target=command_start(message)).start()
            else:
                bot.send_message(
                    chat_id, "Due to some technical issues, your purchase(s) wasn't store properly.\nPlease try again later.")
                finalMsg = """Final shopping cart:\n"""
                Thread(target=command_start(message)).start()
    except Exception as e:
        bot.reply_to(message, 'oooops')

# JOIN
# send UCD, take bubble ID
# send user take userID
# Send qty col.... Take itemID
# send order transsaction ID

# /edit commmand
#ask for ptn
@bot.message_handler(commands=['edit'])
def command_edit(m):
    cid = m.chat.id
    Edititem[0] = cid
    bot.send_chat_action(cid, 'typing')
    msg = bot.reply_to(
        m, """Hey there, change of mind? No problem! Can we have your Personal Transaction Number (PTN) for your purchase please?""")
    bot.register_next_step_handler(msg, edit_choice)

# retrieve all item relate to PTN
def edit_choice(m):
    try:
        cid = m.chat.id
        PTN = m.text
        if m.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            PTN = m.text
            Edititem[0] = PTN
            print(Edititem[0])
            Edititem[2] = database.edit_get_item(Edititem[0])
            print(((Edititem[2])[0])[1])
            count = 1
            send_msg = """Which item do you want to edit?
"""
            for x in Edititem[2]:
                send_msg = send_msg + str(count) + ")" + x[1]+"\n"
                count = count + 1
            markup16 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('1')
            itembtn2 = types.KeyboardButton('2')
            itembtn3 = types.KeyboardButton('3')
            itembtn4 = types.KeyboardButton('4')
            itembtn5 = types.KeyboardButton('5')
            itembtn6 = types.KeyboardButton('Cancel')
            markup16.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)
            msg = bot.reply_to(m, send_msg, reply_markup=markup16)
            bot.register_next_step_handler(msg, edit_properties)
    except Exception as e:
        bot.reply_to(m, 'oooops')

# store choice and ask for properties to edit
def edit_properties(m):
    try:
        cid = m.chat.id
        if m.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            choice = m.text
            Edititem[3] = choice
            print(choice)
            markup17 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
            itembtn1 = types.KeyboardButton('Quantity')
            itembtn2 = types.KeyboardButton('Size')
            itembtn3 = types.KeyboardButton('Colour')
            itembtn4 = types.KeyboardButton('Delete')
            itembtn5 = types.KeyboardButton('Cancel')
            markup17.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
            msg = bot.reply_to(
                m, """Which properties you want to change?""", reply_markup=markup17)
            bot.register_next_step_handler(msg, edit_changes)
    except Exception as e:
        bot.reply_to(m, 'oooops')

# store properties and ask for the changes
def edit_changes(m):
    try:
        cid = m.chat.id
        if m.text == 'Cancel':
            Thread(target=command_start(message)).start()
        else:
            properties = m.text
            Edititem[4] = properties
            print(properties)
            msg = bot.reply_to(m, """The changes would be?""")
            bot.register_next_step_handler(msg, edit_end)
    except Exception as e:
        bot.reply_to(m, 'oooops')

# store the changes and use the edit function
def edit_end(m):
    try:
        cid = m.chat.id
        changes = m.text
        Edititem[5] = changes
        print(changes)
        chooser = int(Edititem[3]) - 1
        itemID = ((Edititem[2])[chooser])[0]
        print(itemID)
        if (database.edit_item(itemID, Edititem[4], Edititem[5])):
            bot.send_message(cid, """Successfull edited your item""")
        else:
            bot.send_message(cid, """Unsuccessful""")
    except Exception as e:
        bot.reply_to(m, 'oooops')


# edit
# send PTN, take all item name and item id
# ask which item, storelocal
# ask color qty..... store local
# send to database...

@bot.message_handler(commands=['faq'])
def command_faq(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    bot.send_message(cid,
                     """Hello! Here is an exhaustive list of FAQ that our users have for us. Take a quick look!

Who are we?
Buyn is a social shopping platform working out of I3. We hope to connect shoppers together with a user-centric focused framework. Buyn is currently working with the support of NUS Enterprise. Check out our insta page for more details at @officialbuyn and leave us comments on how to be better. :-)

When do I make payments?
You will only be required to make payments when your Cart is filled and ready to go. Get your friends to help you with filling the Cart!

Which payment options are available?
We currently only accepts PayNow. So sorry for the inconvenience! 

How do I return my products?
For product returns, Buyn will follow the existing individual company policies that you are shopping out from. Please contact a Buyn admin via /return if you would like to return a product. :-)

I want to shop at a brand which is not here. What can I do?
Please tell us how to best expand our brand list here /recommendbrands. We look forward to hearing from you amigo! 

How long do I have to wait?
Each Cart lasts for 24hours, we will inform you once the Cart reaches 80% of its stipulated goal. Sit back and relax while your Cart fills :-)

What if my Cart doesnt fill?
You can have the option to extend your Cart’s waiting time or cancel your order. Although we do prefer the former!""")


@bot.message_handler(commands=['brandlist'])
def command_brandlist(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    bot.send_message(cid,
                     """Current brands on Buyn and their minimum basket size to qualify for free shipping!
1.	Colorpop: $50 💄
2.	Sephora: $40 [FREE SHIPPING] $110 [FREE NEXT DAY] 💄
3.	Uniqlo: $60 👚
4.	Zara: $79 👚
5.	The Editor’s Market: 3 pieces and more, discounts up to 6 pieces. 👚
6.	The Tinsel Rack: $100 👚
7.	Abercrombie & Fitch: $160 👚
8.	Love, Bonito: Nil 👚
9.	Gardenpicks: $50 🥜
10.	MyProtein: $100 💊""")

# help page


@bot.message_handler(commands=['help'])
def command_help(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')  # show the bot "typing" (max. 5 secs)
    time.sleep(2)
    bot.send_message(cid,
                     """Hey there! This is a list of commands you can use readily :-)

/create: Create a new Cart to share with your friends.

/join: Join an existing Cart :-)

/edit: To edit your order!

/brandlist: A list of existing brands that is working on Buyn right now!

/recommendbrand: Tell us who should be here! 

We hope this helps. If you have any further queries feel free to visit our /faq section!
""")

@bot.message_handler(commands=['recommendbrand'])
def command_recommend(m):
    try:
        cid = m.chat.id
        bot.send_chat_action(cid, 'typing')    
        msg = bot.reply_to(m, """Hey there! Please tell us your desired brand who is not currently on the platform.""")
        bot.register_next_step_handler(msg, recommend_input)
    except Exception as e:
        bot.reply_to(m, 'oooops')

def recommend_input(m):
    try:
        cid = m.chat.id
        telegram_handle = m.chat.username
        brand = m.text
        database.add_user(cid, telegram_handle, m.chat.first_name)
        print(brand)
        if (database.recommend(telegram_handle, brand)):
            bot.send_message(cid, """Thank You""")
        else:
            bot.send_message(cid, """Sorry, there's some technical issues so the recommended brand wasn't stored""")
    except Exception as e:
        bot.reply_to(m, 'oooops')

@bot.message_handler(commands=['statue'])
def command_statue(m):
    try:
        cid = m.chat.id
        markup18 = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        itembtn1 = types.KeyboardButton('Query your bubble')
        itembtn2 = types.KeyboardButton('Query the bubble statue')
        itembtn3 = types.KeyboardButton('Query my items')
        itembtn4 = types.KeyboardButton('Query my address')
        markup18.add(itembtn1, itembtn2, itembtn3, itembtn4)
        msg = bot.reply_to(
            m, """What you want to query?""", reply_markup=markup18)
        bot.register_next_step_handler(msg, statue_input)
    except Exception as e:
        bot.reply_to(m, 'oooops')

def statue_input(m):
    try:
        cid = m.chat.id
        if (m.text == 'Query your bubble'):
            msg = bot.reply_to(m, "Can i have your username?")
            bot.register_next_step_handler(msg, statue_bubble)
        elif(m.text == 'Query the bubble statue'):
            msg = bot.reply_to(m, "Can i have your UCN?")
            bot.register_next_step_handler(msg, statue_bubbleStatue)
        elif(m.text == 'Query my items'):
            msg = bot.reply_to(m, "Can i have your username?")
            bot.register_next_step_handler(msg, statue_item)
        elif(m.text == 'Query my address'):
            msg = bot.reply_to(m, "Can i have your username?")
            bot.register_next_step_handler(msg, statue_address)
    except Exception as e:
        bot.reply_to(m, 'oooops')

def statue_bubble(m):
    try:
        print(m.text)
        print(database.query_joined_bubbles(m.text))
        list = database.query_joined_bubbles(m.text)
        msg = ""
        for x in list:
            msg = msg + x[0] + ":" + x[1] + "\n"
        print(msg)
        bot.send_message(m.chat.id, """Your UCN and PTN:
""" + msg)
    except Exception as e:
        bot.reply_to(m, 'oooops')

def statue_bubbleStatue(m):
    try:
        print(m.text)
        retailer, currentAmount, neededAmount = database.query_bubble_status(m.text)
        print(database.query_bubble_status(m.text))
        bot.send_message(m.chat.id, ("""Your current """+ retailer + """ cart is """ + str(currentAmount) + """/""" + str(neededAmount)))
    except Exception as e:
        bot.reply_to(m, 'oooops')       
def statue_item(m):
    try:
        print(m.text)
        print(database.query_items(m.text))
        list = database.query_items(m.text)
        msg = ""
        for x in list:
            msg = msg + "PTN: " + x[0] + "\nRetailer: " + x[1] + "\nProduce name: " + x[2] + "\nPrice: " + str(x[3]) + "\nSize: " + x[4] + "\nColour: " + x[5] + "\nQuantity: "+ str(x[6]) + "\n\n"
        print(msg)
        bot.send_message(m.chat.id, msg)
    except Exception as e:
        bot.reply_to(m, 'oooops')       
def statue_address(m):
    try:
        print(m.text)
        if (database.address_exist(m.text) == False):
            bot.send_message(m.chat.id, "Sorry, there is no address registered under this username")
        else:
            bot.send_message(m.chat.id, "Your current address is " + database.address_exist(m.text))
        print(database.address_exist(m.text))
    except Exception as e:
        bot.reply_to(m, 'oooops')       




# filter on a specific message


@bot.message_handler(func=lambda message: message.text == "hi")
def command_text_hi(m):
    bot.send_message(m.chat.id, "I love you too!")


# default handler for every other text
@bot.message_handler(func=lambda message: True, content_types=['text'])
def command_default(m):
    # this is the standard reply to a normal message
    bot.send_message(m.chat.id, "I don't understand \"" +
                     m.text + "\"\nMaybe try the help page at /help")


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()


bot.polling()
