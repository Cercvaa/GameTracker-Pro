import sqlite3,mysql.connector,requests,bs4,json,asyncio
from bs4 import BeautifulSoup
from config import SERVER_LIMIT, DATABASE_NAME

print(DATABASE_NAME, SERVER_LIMIT)


class Database():
    def __init__(self, guild : int):
        self.guild = guild
        self.database = []

    def check(self):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        count = 0

        c.execute(f"SELECT * FROM users WHERE guild_id = {str(self.guild)}")
        results = c.fetchall()
        for result in results:
            if result[0] == str(self.guild):
                count += 1
            else:
                count = 0


        if count < SERVER_LIMIT: return True
        elif count == SERVER_LIMIT: return False
        conn.commit()

    def checklog(self):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        count_log = 0

        results = c.execute(f"SELECT * FROM log WHERE guild_id = {str(self.guild)}").fetchall()

        for result in results:
            if result[0] == str(self.guild):
                count_log += 1
            else:
                count_log = 0

        if count_log == 0 or count_log == 1 or count_log == 2 or count_log == 3 or count_log == 4: return True
        elif count_log == 5: return False
        conn.commit()
    """
    def checkip(self, ip : str):
        conn = sqlite3.connect("data.db")

        c = conn.cursor()

        ip_count = 0

        results = c.execute(f"SELECT ip FROM users WHERE guild_id = {str(self.guild)}").fetchall()
        conn.commit()
        for result in results:
            if result[0] == ip:
                ip_count += 1
        
        if ip_count == 1:
            return False
        else:
            return True

    """

    def checkvoiceip(self, ip : str):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        ip_count = 0

        c.execute(f"SELECT ip FROM voice WHERE guild_id = {str(self.guild)}")
        results = c.fetchall()
        for result in results:
            if result[0] == ip:
                ip_count += 1
        
        if ip_count == 1:
            return False
        else:
            return True

        conn.commit()

    def delvcip(self, ip : str):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()
        check = False
        
        c.execute(f"SELECT guild_id FROM voice WHERE ip = '{ip}'")
        result = c.fetchone()
        if result[0] == str(self.guild): check = True
        else: check = False

        return check 
        conn.commit()

    def delip(self, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        #fix this 
        check = False
        #fix this 
        c.execute(f"SELECT ip FROM users WHERE id = {str(id)}")
        result = c.fetchone()
        if result is None:
            check = False
        else:
            check = True

        return check
        conn.commit()


    def delchannel(self, channel : int):
        conn = sqlite3.connect(DATABASE_NAME)

        c = conn.cursor()

        checkguild = False

        c.execute(f"SELECT guild_id FROM log WHERE channel_id = {channel}")
        result = c.fetchone()

        if result[0] == str(self.guild): checkguild = True
        else: checkguild = False

        return checkguild
        conn.commit()

    def delvoiceip(self, ip : str):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        check = False
        c.execute(f"SELECT guild_id FROM voice WHERE ip = '{ip}'")
        result = c.fetchone()
        if result[0] == str(self.guild): check = True
        else: check = False

        return check
        conn.commit()


    def fetchid(self, ip : str, id : int):
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()

        check = False
        c.execute(f"SELECT id FROM users WHERE guild_id = '{str(self.guild)}' AND ip = '{ip}'")
        results = c.fetchall()
    
        for result in results:
            print(result[0])
            if result[0] == str(id):
                check = True
            else:
                check = False

        return check
        conn.commit()
