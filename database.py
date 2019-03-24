import settings
import mysql.connector as mysql
import random
import string
import requests
from collections import defaultdict

db = mysql.connect(
    host = settings.host,
    user = settings.user,
    passwd = settings.passwd,
    database = settings.database
)

c = db.cursor()

def bot_sendtext(bot_chatID, bot_message):
    try:	
        # Send text message
        bot_token = settings.notification_bot_token
        send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + str(bot_chatID) + '&parse_mode=Markdown&text=' + bot_message 
        requests.get(send_text)
    except:
        return False

def bubble_full_request_payment(bubble_id):
    try:
        # Get chat ids of users and accompanying variables for users' orders in bubble
        c.execute('''SELECT chat_id, first_name, retailer_name, ucn, total_price, quantity, item_name FROM orders 
                    INNER JOIN users USING (user_id)
                    INNER JOIN bubbles USING (bubble_id)
                    INNER JOIN retailers USING (retailer_id)
                    INNER JOIN items USING (item_id)
                    WHERE bubble_id = %s''', (bubble_id,))
        bubble_users_list = c.fetchall()
        
        # Send users in full bubbles payment request
        # Create dictionary of users with list of lists of their items
        bubble_users_dict = defaultdict(list)
        for bubble_user in bubble_users_list:
            bot_chatID, first_name, retailer_name, ucn, total_price, quantity, item_name = bubble_user
            bubble_users_dict[bot_chatID].append([first_name, retailer_name, ucn, total_price, quantity, item_name])

        # Create bot_message
        for bot_chatID in bubble_users_dict:
            print(bot_chatID)
            first_name, retailer_name, ucn, _, _, _ = bubble_users_dict[bot_chatID][0]
            total_price_to_pay = 0
            bot_message = f"Hi {first_name}, your {retailer_name} cart {ucn} has been filled\nYou ordered:\n"
            for item_list in bubble_users_dict[bot_chatID]:
                _, _, _, total_price, quantity, item_name = item_list
                total_price_to_pay += total_price
                bot_message += f"{item_name} of quantity {quantity} for {total_price}\n"
            bot_message += f"Please make payment of {total_price_to_pay} to 9123123123 by PayLah!"
            print(bot_message)
            bot_sendtext(bot_chatID, bot_message)

        return True 
    except:
        return False

def bubble_full(bubble_id):
    try:
        # Check if bubble is full
        c.execute('''SELECT cart_amount, free_shipping_amount, filled_date FROM bubbles
                    INNER JOIN retailers USING (retailer_id)
                    WHERE bubble_id = %s LIMIT 1''', (bubble_id,))
        cart_amount, free_shipping_amount, filled_date = c.fetchone()
        print('cart amount:', cart_amount)
        print('shipping amount:', free_shipping_amount)
        # Update filled_date if bubble is filled and request payment from users
        if cart_amount >= free_shipping_amount:
            if filled_date is None:
                c.execute('UPDATE bubbles SET filled_date = NOW() WHERE bubble_id = %s', (bubble_id,))
                db.commit() 
                bubble_full_request_payment(bubble_id)
            print("bubble full: " + str(cart_amount) + "/" + str(free_shipping_amount))    
            
            return True
        else: 
            c.execute('UPDATE bubbles SET filled_date = NULL WHERE bubble_id = %s', (bubble_id,))
            db.commit()             
            print('bubble not full: ' + str(cart_amount) + "/" + str(free_shipping_amount))  
            return False
    except:
        return False

def add_user(chat_id, telegram_handle, first_name):
    # Check if user exists
    c.execute("SELECT user_id FROM users WHERE chat_id = %s LIMIT 1", (chat_id,))
    try:
        # User exist
        user_id = c.fetchone()[0]
        print('user exists')
    except:
        # User does not exist, add into users table
        query = 'INSERT INTO users (chat_id, telegram_handle, first_name) VALUES (%s, %s, %s)'
        values = (chat_id, telegram_handle, first_name)
        c.execute(query, values)
        db.commit()
        user_id = c.lastrowid
        print('user added')
    
    return user_id 

def add_retailer(retailer_name, acronym, website, free_shipping_amount):
    try:
        # Check if retailer exists
        c.execute("SELECT retailer_id FROM retailers WHERE website = %s LIMIT 1", (website,))        
        # Retailer exist
        retailer_id = c.fetchone()[0]
    except:
        # Retailer does not exist, add into retailers table
        query = 'INSERT INTO retailers (retailer_name, acronym, website, free_shipping_amount) VALUES (%s, %s, %s, %s)'
        values = (retailer_name, acronym, website, free_shipping_amount)
        c.execute(query, values)
        db.commit()
        retailer_id = c.lastrowid

    return retailer_id 
    
def add_bubble(retailer_id, user_id, bubble_type):
    try:
        # Check if retailer and user id exists
        c.execute("SELECT acronym FROM retailers WHERE retailer_id = %s LIMIT 1", (retailer_id,))
        acronym = c.fetchone()[0]
        c.execute("SELECT user_id FROM users WHERE user_id = %s LIMIT 1", (user_id,))
        c.fetchone()[0]
        print('acronym',acronym)

        # generate UCN and add new row
        ucn = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(4)]) 
        ucn_last = ''
        if bubble_type == 'Private':
            ucn_last = 'PRI'
        elif bubble_type == 'Public':
            ucn_last = 'PUB'
        ucn = acronym + ucn + ucn_last   
        print('ucn: ',ucn)
        query = 'INSERT INTO bubbles (ucn, retailer_id, user_id, bubble_type) VALUES (%s, %s, %s, %s)'
        values = (ucn, retailer_id, user_id, bubble_type)
        c.execute(query, values)
        db.commit()
        bubble_id = c.lastrowid
        print('bubble added')

        return bubble_id, ucn
    except:
        return False

def add_item(retailer_id, web_link, item_name, unit_price, size, color, quantity):
    try:
        # Check if retailer id exists
        c.execute("SELECT retailer_id FROM retailers WHERE retailer_id = %s LIMIT 1", (retailer_id,))
        c.fetchone()[0]

        # Add item into items table
        query = '''INSERT INTO items (retailer_id, web_link, item_name, unit_price, size, color, quantity, total_price) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
        values = (retailer_id, web_link, item_name, unit_price, size, color, quantity, unit_price*quantity)
        c.execute(query, values)
        db.commit()
        print('item added')
        item_id = c.lastrowid
    
        return item_id 
    except:
        return False

def add_order(bubble_id, user_id, item_id, shipping_location):
    try:
        # Check if user and item id exists
        c.execute("SELECT user_id FROM users WHERE user_id = %s LIMIT 1", (user_id,))
        c.fetchone()[0]
        c.execute("SELECT item_id FROM items WHERE item_id = %s LIMIT 1", (item_id,))
        c.fetchone()[0]

        # generate PTN and add row
        c.execute('''SELECT acronym, user_id, bubble_type FROM bubbles 
                    INNER JOIN retailers USING (retailer_id) 
                    WHERE bubble_id = %s LIMIT 1''', (bubble_id,))
        acronym, bubble_creator_id, bubble_type = c.fetchone()
        print('bubble type',bubble_type)
        ptn = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(4)])
        ptn_last = ''
        if bubble_type == 'Private':
            ptn_last = 'PRI'
            # Get bubble creator address
            c.execute('SELECT address FROM users WHERE user_id = %s LIMIT 1', (bubble_creator_id,))
            bubble_creator_address = c.fetchone()[0]
            print('bubble creator address: ', bubble_creator_address)

            # Update user's address if user is bubble creator, else, use bubble creator address as shipping location
            if bubble_creator_id == user_id and bubble_creator_address is None:
                c.execute('UPDATE users SET address = %s WHERE user_id = %s', (shipping_location, user_id))
                db.commit()
            else:
                shipping_location = bubble_creator_address
        elif bubble_type == 'Public':
            if shipping_location == 'UTown':
                ptn_last = 'UT'
            if shipping_location == 'CLB':
                ptn_last = 'CLB' 
        ptn = acronym + ptn + ptn_last  
        print('ptn:', ptn)     
        query = 'INSERT INTO orders (bubble_id, user_id, item_id, ptn, shipping_location) VALUES (%s, %s, %s, %s, %s)'
        values = (bubble_id, user_id, item_id, ptn, shipping_location)        
        c.execute(query, values)
        db.commit()
        print('order added')

        # update bubble amount
        add_to_bubble_amount(bubble_id, item_id)
        bubble_full(bubble_id)

        return ptn
    except:
        return False 

def recommend_brand(telegram_handle, brand):
    try:
        c.execute('SELECT user_id FROM users WHERE telegram_handle = %s LIMIT 1', (telegram_handle,))
        user_id = c.fetchone()[0]
        c.execute('INSERT INTO recommendations (user_id, brand) VALUES (%s, %s)', (user_id, brand))
        db.commit()  

        return True
    except:
        return False

def replace_ptn(ptn, bubble_id, user_id):
    # Change all PTN to given PTN for those with same bubble and user id
    try:
        c.execute('UPDATE orders SET ptn = %s WHERE bubble_id = %s AND user_id = %s', (ptn, bubble_id, user_id))
        db.commit()

        return True 
    except:
        return False

def retrieve_bubble(ucn):
    # Retrieve bubble and retailer id for particular UCN
    try:
        c.execute('SELECT bubble_id, retailer_id FROM bubbles WHERE ucn = %s LIMIT 1', (ucn,))
        bubble_id, retailer_id = c.fetchone()

        return bubble_id, retailer_id
    except:
        return False

def edit_get_item(ptn):
    # for particular PTN, retrieve all items with that PTN
    try:
        c.execute('''SELECT item_id, item_name FROM orders
                    INNER JOIN items USING (item_id)
                    WHERE ptn = %s''', (ptn,))
        item_list = c.fetchall()

        return item_list
    except:
        return False

def edit_item(item_id, column_to_change, value_to_change):
    try:
        # Check if item_id exists
        c.execute("SELECT item_id FROM items WHERE item_id = %s LIMIT 1", (item_id,))
        c.fetchone()[0]        

        # Edit column value based on column specified
        if column_to_change == 'Size':
            c.execute('UPDATE items SET size = %s WHERE item_id = %s', (value_to_change, item_id))

        elif column_to_change == 'Colour':
            c.execute('UPDATE items SET color = %s WHERE item_id = %s', (value_to_change, item_id))

        elif column_to_change == 'Delete':
            # Get total price
            c.execute('SELECT total_price FROM items WHERE item_id = %s', (item_id,))
            total_price = c.fetchone()[0]

            # Update cart amount in bubbles table
            c.execute('SELECT bubble_id FROM orders WHERE item_id = %s', (item_id,)) 
            bubble_id = c.fetchone()[0]
            c.execute('''UPDATE bubbles SET cart_amount = cart_amount - %s 
                        WHERE bubble_id = %s''', (total_price, bubble_id))

            # Delete item which deletes order
            c.execute('DELETE FROM items WHERE item_id = %s', (item_id,)) 

            bubble_full(bubble_id)   

        elif column_to_change == 'Quantity':
            c.execute('UPDATE items SET quantity = %s WHERE item_id = %s', (value_to_change, item_id))
            # Get unit price
            c.execute('SELECT unit_price FROM items WHERE item_id = %s', (item_id,))
            unit_price = c.fetchone()[0]

            # Get current total price
            c.execute('SELECT total_price FROM items WHERE item_id = %s', (item_id,))
            current_total_price = c.fetchone()[0]

            # Update total price for items table
            new_total_price = int(value_to_change) * unit_price
            c.execute('UPDATE items SET total_price = %s WHERE item_id = %s', (new_total_price, item_id))

            # Update cart amount in bubbles table
            c.execute('SELECT bubble_id FROM orders WHERE item_id = %s', (item_id,)) 
            bubble_id = c.fetchone()[0]
            c.execute('''UPDATE bubbles SET cart_amount = cart_amount + %s - %s 
                        WHERE bubble_id = %s''', (new_total_price, current_total_price, bubble_id))
            bubble_full(bubble_id)

        elif column_to_change == 'Price':
            c.execute('UPDATE items SET unit_price = %s WHERE item_id = %s', (value_to_change, item_id))
            # Get quantity
            c.execute('SELECT quantity FROM items WHERE item_id = %s', (item_id,))
            quantity = c.fetchone()[0]

            # Get current total price
            c.execute('SELECT total_price FROM items WHERE item_id = %s', (item_id,))
            current_total_price = c.fetchone()[0]

            # Update total price for items table
            new_total_price = int(value_to_change) * quantity
            c.execute('UPDATE items SET total_price = %s WHERE item_id = %s', (new_total_price, item_id))

            # Update cart amount in bubbles table
            c.execute('SELECT bubble_id FROM orders WHERE item_id = %s', (item_id,)) 
            bubble_id = c.fetchone()[0]
            c.execute('''UPDATE bubbles SET cart_amount = cart_amount - %s + %s 
                        WHERE bubble_id = %s''', (current_total_price, new_total_price, bubble_id))
            bubble_full(bubble_id)

        db.commit()

        return True
    except:
        return False

def add_to_bubble_amount(bubble_id, item_id):
    try:
        # get item total price
        c.execute('SELECT total_price FROM items WHERE item_id = %s', (item_id,))
        total_price = c.fetchone()[0]

        # update bubble amount
        c.execute('UPDATE bubbles SET cart_amount = cart_amount + %s WHERE bubble_id = %s', (total_price, bubble_id))
        db.commit()

        return True
    except:
        return False

def query_joined_bubbles(telegram_handle):
    try:
        # for a particular user, return a list of UCN and PTN user is in 
        c.execute('''SELECT ucn, ptn FROM orders 
                    INNER JOIN users USING (user_id)
                    INNER JOIN bubbles USING (bubble_id)
                    WHERE telegram_handle = %s''', (telegram_handle,))
        bubble_list = c.fetchall()
        # remove duplicates
        bubble_list = list(dict.fromkeys(bubble_list))

        return bubble_list
    except:
        False

def query_bubble_status(ucn):
    try:
        # for a bubble given by UCN, return the amount and amount to hit for that bubble
        c.execute('''SELECT retailer_name, cart_amount, free_shipping_amount FROM bubbles 
                    INNER JOIN retailers USING (retailer_id) 
                    WHERE ucn = %s''', (ucn,))
        retailer_name, cart_amount, free_shipping_amount = c.fetchone()

        return retailer_name, cart_amount, free_shipping_amount
    except:
        False

def query_items(telegram_handle):
    try:
        # for a particular user, return the items user have placed
        c.execute('''SELECT ucn, retailer_name, item_name, unit_price, size, color, quantity FROM orders 
                    INNER JOIN items USING (item_id)
                    INNER JOIN retailers USING (retailer_id)
                    INNER JOIN users USING (user_id)
                    INNER JOIN bubbles USING (bubble_id)
                    WHERE telegram_handle = %s''', (telegram_handle,))
        item_list = c.fetchall()

        return item_list
    except:
        False

def update_stage(telegram_handle, latest_stage):
    try:
        c.execute('''UPDATE users SET latest_stage = %s 
                    WHERE telegram_handle = %s''', (latest_stage, telegram_handle))
        c.execute('''UPDATE users SET highest_stage = %s 
                    WHERE latest_stage > highest_stage 
                    && telegram_handle = %s''', (latest_stage, telegram_handle))
        db.commit()

        return True
    except:
        return False

def address_exist(telegram_handle):
    try:
        c.execute('SELECT address FROM users WHERE telegram_handle = %s LIMIT 1', (telegram_handle,))
        address = c.fetchone()[0]
        if address is None:
            return False

        return address
    except:
        return False

def edit_address(telegram_handle, address):
    try:
        c.execute('UPDATE users SET address = %s WHERE telegram_handle = %s', (address, telegram_handle))
        db.commit()

        return True
    except:
        return False


# TO DO
'''
1. TIMESTAMP no default value allowed in server? no more than 2 CURRENT TIME
'''

# Run functions
#print(bubble_full(2))                                        #bubble_id

#print(bubble_full_request_payment(1))                         #bubble_id

#print(add_user(settings.admin1, 'jonasanderson', 'Jonas'))         #chat_id, telegram_handlr, first_name
#print(add_user(1234, 'timmydoc', 'Timmy'))  

add_retailer('Uniqlo', 'UNQ', 'https://www.uniqlo.com', 60)   #retailer_name, acronym, website, free_shipping_amount
add_retailer('ColourPop', 'CLP', 'https://colourpop.com/', 50)
add_retailer('Zalora', 'ZLR', 'https://www.zalora.sg', 40)
add_retailer('The Editors Market', 'TEM', 'https://www.theeditorsmarket.com/', 60)
add_retailer('The Tinsel Rack', 'TTR', 'https://www.thetinselrack.com/', 100)
add_retailer('Abercrombie And Fitch', 'ANF', 'https://www.abercrombie.sg/en_SG/home', 160)
add_retailer('Myprotein', 'MPT', 'https://www.myprotein.com.sg/', 100)

#print(add_bubble(1, 1, 'Private'))                            #retailer_id, user_id, bubble_type

#print(add_item(1, 'www.blah1.com', 'purple tee', 20, 'EU 34', 'purple', 2))    #retailer_id, web_link, name, unit_price, size, color, quantity
#print(add_item(1, 'www.blah2.com', 'purple tee', 15, 'EU 34', 'purple', 3))

#print(add_order(1, 1, 1, 'pasir ris'))                            #bubble_id, user_id, item_id, shipping_location

#print(retrieve_bubble('UNQ3qIaPRI'))                          #ucn

#print(edit_get_item('ANFwISVCLB'))                            #ptn

#print(edit_item(1, 'delete', 'na'))                           #item_ID, ‘size’, ‘XS

#print(replace_ptn('atRF', 10, 1))                             #last_ptn, bubble_ID, user_ID

#print(query_joined_bubbles('timmydoc'))                       #telegram_handle

#print(query_bubble_status('ANFkS2ePRI'))                      #ucn

#print(query_items('timmydoc'))                                #telegram_handle

#recommend_brand('Jonas', 'uniqlo')                            #telegram_handle, retailer

#print(update_stage('timmydoc', 1))                            #telegram_handle, latest_stage

#print(address_exist('timmydoc'))                              #telegram_handle

#print(edit_address('timmydoc', 'city'))                       #telegram_handle, address