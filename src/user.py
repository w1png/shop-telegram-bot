import sqlite3
from datetime import datetime
import item as itm
from order import Order
from settings import Settings

conn = sqlite3.connect('data.db')
c = conn.cursor()
settings = Settings()

class User:
    def __init__(self, user_id):
        self.__user_id = user_id

        if not does_user_exist(self.get_id()):
            c.execute(f"INSERT INTO users VALUES(?, ?, ?, ?, ?, ?, ?)", [self.get_id(), 1 if str(self.get_id()) == settings.get_main_admin_id() else 0, 0, 0, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "None", 1])
            conn.commit()

    def get_id(self):
        return self.__user_id

    def __clist(self):
        c.execute(f"SELECT * FROM users WHERE user_id=?", [self.get_id()])
        return list(c)[0]

    def is_admin(self):
        return self.__clist()[1] == 1

    def set_admin(self, value):
        c.execute(f"UPDATE users SET is_admin=? WHERE user_id=?", [value, self.get_id()])
        conn.commit()

    def is_manager(self):
        return self.__clist()[2] == 1

    def set_manager(self, value):
        c.execute(f"UPDATE users SET is_manager=? WHERE user_id=?", [value, self.get_id()])
        conn.commit() 
        
    def get_register_date(self):
        return datetime.strptime(self.__clist()[4], "%Y-%m-%d %H:%M:%S")

    def get_register_date_string(self):
        return self.__clist()[4]

    def notif_on(self):
        return self.__clist()[3] == 1

    def set_notif_enable(self, value):
        c.execute(f"UPDATE users SET notification=? WHERE user_id=?", [value, self.get_id()])
        conn.commit()

    def get_orders(self):
        c.execute(f"SELECT * FROM orders WHERE user_id=?", [self.get_id()])
        return list(map(Order, [order[0] for order in list(c)]))[::-1]
    
    def get_cart_comma(self):
        return self.__clist()[5]
    
    def get_cart(self):
        cart = self.get_cart_comma()
        return [] if cart == "None" else list(map(itm.Item, cart.split(",")))
    
    def get_cart_amount(self):
        cart = [item.get_id() for item in self.get_cart()]
        return [[itm.Item(item_id), cart.count(item_id)] for item_id in set(cart)]
    
    def get_cart_price(self):
        return sum([item_and_price[0].get_price() * item_and_price[1] for item_and_price in self.get_cart_amount()]) + (settings.get_delivery_price() if self.is_cart_delivery() else 0)
    
    def clear_cart(self):
        c.execute(f"UPDATE users SET cart=\"None\" WHERE user_id=?", [self.get_id()])
        self.set_cart_delivery(1)
        conn.commit()
        
    def add_to_cart(self, item_id):
        cart = self.get_cart()
        c.execute(f"UPDATE users SET cart=? WHERE user_id=?", [",".join([str(item.get_id()) for item in cart + [itm.Item(item_id)]]) if cart else item_id, self.get_id()])
        conn.commit()
        
    def remove_from_cart(self, item_id):
        cart = [item.get_id() for item in self.get_cart()]
        cart.remove(str(item_id))
        c.execute(f"UPDATE users SET cart=? WHERE user_id=?", [",".join(cart) if cart else "None", self.get_id()])
        conn.commit()
        
    def is_cart_delivery(self):
        return self.__clist()[6] == 1

    def set_cart_delivery(self, value):
        c.execute(f"UPDATE users SET cart_delivery=? WHERE user_id=?", [value, self.get_id()])
        conn.commit()
        

def does_user_exist(user_id):
    c.execute(f"SELECT * FROM users WHERE user_id=?", [user_id])
    return len(list(c)) != 0


def get_notif_list():
    c.execute(f"SELECT * FROM users WHERE notification=1")
    return list(map(User, [user[0] for user in list(c)]))


def get_user_login(message):
    return message.from_user.username


def get_user_list():
    c.execute("SELECT * FROM users")
    return list(map(User, [user[0] for user in list(c)]))
