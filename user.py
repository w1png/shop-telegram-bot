from configparser import ConfigParser
import sqlite3
from configparser import ConfigParser
from datetime import datetime
import item as itm

conn = sqlite3.connect('data.db')
c = conn.cursor()


class User:
    def __init__(self, user_id):
        self.user_id = user_id

        if not does_user_exist(self.get_id()):
            conf = ConfigParser()
            conf.read('config.ini', encoding='utf8')
            c.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?)", [self.get_id(), 0, 1 if str(self.get_id()) == conf["main"]["main_admin_id"] else 0, 0, 0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            conn.commit()

    def get_id(self):
        return self.user_id

    def __clist(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.get_id()}")
        return list(c)[0]

    def is_admin(self):
        return self.__clist()[1] == 1

    def set_admin(self, value):
        c.execute(f"UPDATE users SET is_admin={value} WHERE user_id={self.get_id()}")
        conn.commit()

    def is_support(self):
        return self.__clist()[2] == 1

    def set_support(self, value):
        c.execute(f"UPDATE users SET is_support={value} WHERE user_id={self.get_id()}")
        conn.commit()

    def get_register_date(self):
        return self.__clist()[4]

    def notif_on(self):
        return self.__clist()[3] == 1

    def enable_notif(self):
        c.execute(f"UPDATE users SET notification=1 WHERE user_id={self.get_id()}")

    def disable_notif(self):
        c.execute(f"UPDATE users SET notification=0 WHERE user_id={self.get_id()}")

    def get_orders(self):
        c.execute(f"SELECT * FROM orders WHERE user_id=\"{self.get_id()}\"")
        return list(map(itm.Order, [order[0] for order in list(c)]))


def does_user_exist(user_id):
    c.execute(f"SELECT * FROM users WHERE user_id=\"{user_id}\"")
    return len(list(c)) != 0


def get_notif_list():
    c.execute(f"SELECT * FROM users WHERE notification=1")
    return map(User, [user[0] for user in list(c)])


def get_user_login(message):
    return message.from_user.username


def get_user_list():
    c.execute("SELECT * FROM users")
    return map(User, [user[0] for user in list(c)])
