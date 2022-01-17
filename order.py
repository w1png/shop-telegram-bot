import sqlite3
from datetime import datetime
import item as itm
import text_templates as tt
from settings import Settings

settings = Settings()

conn = sqlite3.connect("data.db")
c = conn.cursor()

class Order:
    def __init__(self, id):
        self.id = id
        
    def __repr__(self):
        return f"{self.get_order_id()}"
    
    def get_order_id(self):
        return self.id
    
    def __clist(self):
        c.execute(f"SELECT * FROM orders WHERE order_id=?", [self.get_order_id()])
        return list(c)[0]
    
    def get_user_id(self):
        return self.__clist()[1]
    
    def get_item_list_raw(self):
        return self.__clist()[2]
    
    def get_item_list(self):
        return list(map(itm.Item, [item_id for item_id in self.get_item_list_raw().split(",")]))
    
    def get_item_list_amount(self):
        cart = [item.get_id() for item in self.get_item_list()]
        return [[itm.Item(item_id), cart.count(item_id)] for item_id in set(cart)]
    
    def get_item_list_price(self):
        return sum([item_and_price[0].get_price() * item_and_price[1] for item_and_price in self.get_item_list_amount()]) + (float(settings.get_delivery_price()) if self.get_home_adress() != None else 0)
    
    def set_item_list(self, value):
        c.execute(f"UPDATE orders SET item_list=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
    def get_email_adress(self):
        return self.__clist()[3]
    
    def set_email_adress(self, value):
        c.execute(f"UPDATE orders SET email_adress=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
    def get_phone_number(self):
        return self.__clist()[4]
    
    def set_phone_number(self, value):
        c.execute(f"UPDATE orders SET phone_number=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
    def get_home_adress(self):
        return self.__clist()[5]
    
    def set_home_adress(self, value):
        c.execute(f"UPDATE orders SET home_adress=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
    def get_additional_message(self):
        return self.__clist()[6]
    
    def get_date(self):
        return datetime.strptime(self.__clist()[7], "%Y-%m-%d %H:%M:%S")

    def get_date_string(self):
        return self.__clist()[7]
    
    def get_status(self):
        return self.__clist()[8]
    
    def get_status_string(self):
        return get_status_dict()[self.__clist()[8]]
    
    def set_status(self, value):
        c.execute(f"UPDATE orders SET status=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
def get_status_dict():
    return {
            0: tt.processing,
            1: tt.delivery,
            2: tt.done,
            -1: tt.cancelled,
        }

def get_order_list(status=None):
    if status:
        c.execute(f"SELECT * FROM orders WHERE status=?", [status])
    else:
        c.execute(f"SELECT * FROM orders")
    return list(map(Order, [order[0] for order in list(c)]))

def does_order_exist(order_id):
    c.execute(f"SELECT * FROM orders WHERE order_id=?", [order_id])
    return len(list(c)) == 1
    
def create_order(order_id, user_id, item_list, email_adress, additional_message, phone_number="None", home_adress="None"):
    c.execute(f"INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [order_id, user_id, item_list, email_adress, phone_number, home_adress, additional_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0])
    conn.commit()
    return Order(order_id)