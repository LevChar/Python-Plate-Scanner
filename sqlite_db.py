import sqlite3
from os import path

def singleton(myClass):
    instances = {}
    def getInstance(*args, **kwargs):
        if myClass not in instances:
            instances[myClass] = myClass(*args, **kwargs)
        return instances[myClass]
    return getInstance

@singleton
class sqlite_db():
    def __init__(self, db_name, log):
        self.logger = log
        self.db_name = db_name + ".db"
        self.db_created = False if not path.exists(self.db_name) else True
        self.db_conn = sqlite3.connect(self.db_name)

        if (not self.db_created):
            self.db_created = True
            self.logger.error("DB " + self.db_name + " created")
            self.create_table()

    def create_table(self):
        try:
            self.db_conn.execute("CREATE TABLE vehicle_entry_registration("
                            "plate INTEGER NOT NULL, "
                            "car_type TEXT NOT NULL, "
                            "entry_date TEXT NOT NULL UNIQUE, "
                            "entry_status INTEGER NOT NULL, "
                            "PRIMARY KEY (plate, entry_date));")

            self.db_conn.commit()
            self.logger.error("Table created")

        except sqlite3.OperationalError as e:
            print("Table couldn't be created: ", str(e))

    def add_vehicle_to_db(self, details):
        try:
            cursor = self.db_conn.cursor()
            insert_with_param = """INSERT INTO 'vehicle_entry_registration'
                                     ('plate', 'car_type', 'entry_date', 'entry_status') 
                                     VALUES (?, ?, ?, ?);"""
            cursor.execute(insert_with_param, details)
            self.db_conn.commit()
            self.logger.error("Added entry of 1 vehicle ")
            cursor.close()

        except sqlite3.Error as e:
            print("Couldn't Add vehicle entry: " + str(e))

    def view_db(self):
        cur = self.db_conn.cursor()
        cur.execute("SELECT * FROM vehicle_entry_registration")
        rows = cur.fetchall()

        for row in rows:
            print(row)

        cur.close()