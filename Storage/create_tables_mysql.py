import mysql.connector

db_conn = mysql.connector.connect(host="127.0.0.1", user="root",
password="Mahomeboy#15", database="events")

db_cursor = db_conn.cursor()

db_cursor.execute('''
    CREATE TABLE sale_item
    (item_id INT NOT NULL AUTO_INCREMENT,
    product_name VARCHAR(250) NOT NULL,
    price FLOAT NOT NULL,
    manufacturer VARCHAR(250) NOT NULL,
    rating INTEGER NOT NULL,
    num_times_bought_before VARCHAR(100) NOT NULL,
    date_sold DATETIME NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT sale_item_pk PRIMARY KEY(item_id))
''')

db_cursor.execute('''
    CREATE TABLE num_sales
    (sale_id INT NOT NULL AUTO_INCREMENT,
    profits VARCHAR(250) NOT NULL,
    num_items_sold INTEGER NOT NULL,
    num_vans_needed INTEGER NOT NULL,
    average_rating INTEGER NOT NULL,
    trace_id VARCHAR(250) NOT NULL,
    CONSTRAINT num_sales_pk PRIMARY KEY(sale_id))
''')

db_conn.commit()
db_conn.close()