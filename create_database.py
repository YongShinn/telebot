import settings
import mysql.connector as mysql

# Create buyn database
db = mysql.connect(
    host = settings.host,
    user = settings.user,
    passwd = settings.passwd
)
c = db.cursor()
query = 'CREATE DATABASE IF NOT EXISTS ' + settings.database
c.execute(query)

# Create tables
db = mysql.connect(
    host = settings.host,
    user = settings.user,
    passwd = settings.passwd,
    database = settings.database
)

c = db.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    chat_id INT(11),
    telegram_handle VARCHAR(255) NOT NULL, 
    first_name VARCHAR(255) NOT NULL, 
    address VARCHAR(255) NULL,
    latest_stage TINYINT UNSIGNED,
    highest_stage TINYINT UNSIGNED,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP NULL,
    UNIQUE (chat_id)
)''')

#stage DEFAULT 0
#last_update TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP

# Create retailers table 
c.execute('''CREATE TABLE IF NOT EXISTS retailers (
    retailer_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    retailer_name VARCHAR(255), 
    acronym VARCHAR(255),
    website VARCHAR(255) NOT NULL, 
    free_shipping_amount DECIMAL(8,2) UNSIGNED NOT NULL, 
    last_update TIMESTAMP NULL ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (website)
)''')

# Create bubbles table
c.execute('''CREATE TABLE IF NOT EXISTS bubbles (
    bubble_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    ucn VARCHAR(255) NOT NULL, 
    retailer_id INT(11) UNSIGNED, 
    user_id INT(11) UNSIGNED, 
    cart_amount DECIMAL(8,2) UNSIGNED NOT NULL DEFAULT 0, 
    bubble_type VARCHAR(255), 
    created_at TIMESTAMP NULL,
    filled_date TIMESTAMP NULL, 
    paid_date TIMESTAMP NULL, 
    ordered_date TIMESTAMP NULL, 
    received_shipment_date TIMESTAMP NULL, 
    delivered_date TIMESTAMP NULL, 
    last_update TIMESTAMP NULL,
    FOREIGN KEY (retailer_id) REFERENCES retailers(retailer_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    unique (ucn)    
)''')  

#created at DEFAULT CURRENT_TIMESTAMP

# Create items table
c.execute('''CREATE TABLE IF NOT EXISTS items (
    item_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,     
    retailer_id INT(11) UNSIGNED, 
    web_link VARCHAR(255),
    item_name VARCHAR(255), 
    unit_price DECIMAL(8,2) UNSIGNED,     
    size VARCHAR(255), 
    color VARCHAR(255),
    quantity SMALLINT UNSIGNED,
    total_price DECIMAL(8,2) UNSIGNED,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    last_update TIMESTAMP NULL,
    FOREIGN KEY (retailer_id) REFERENCES retailers(retailer_id)
)''')

# Create orders table
c.execute('''CREATE TABLE IF NOT EXISTS orders (
    order_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    bubble_id INT(11) UNSIGNED, 
    user_id INT(11) UNSIGNED, 
    item_id INT(11) UNSIGNED, 
    ptn VARCHAR(255), 
    shipping_location VARCHAR(255) NULL,
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
    paid_date TIMESTAMP NULL,
    FOREIGN KEY (bubble_id) REFERENCES bubbles(bubble_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE CASCADE  
)''')

# Create recommendations table
c.execute('''CREATE TABLE IF NOT EXISTS recommendations (
    recommendation_id INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    user_id INT(11) UNSIGNED,
    brand VARCHAR(255) NOT NULL, 
    created_at TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP
)''')
