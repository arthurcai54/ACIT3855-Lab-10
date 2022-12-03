import sqlite3
conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()

c.execute('''
        CREATE TABLE max_stats
        (id INTEGER PRIMARY KEY ASC,
        highest_price FLOAT NOT NULL,
        maximum_rating INTEGER NOT NULL,
        max_num_items_sold INTEGER NOT NULL,
        max_num_times_bought_before VARCHAR(100) NOT NULL,
        max_num_vans_needed INTEGER NOT NULL,
        last_updated VARCHAR(100) NOT NULL)
        ''')


conn.commit()
conn.close()