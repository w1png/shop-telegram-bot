import sqlite3
from datetime import datetime

conn = sqlite3.connect("data.db")
c = conn.cursor()


def does_item_exist(item_id):
    c.execute(f"SELECT * FROM items WHERE id={item_id}")
    return len(list(c)) == 1


class Item:
    def __init__(self, item_id):
        self.item_id = item_id
        
    def __eq__(self, __o: object):
        return self.get_id() == __o.get_id()
    
    def __repr__(self):
        return f"[{self.get_id()}] {self.get_name()}"

    def get_id(self):
        return self.item_id
    
    def __clist(self):
        c.execute(f"SELECT * FROM items WHERE id={self.get_id()}")
        return list(c)[0]

    def get_name(self):
        return self.__clist()[1]

    def set_name(self, value):
        c.execute(f"UPDATE items SET name=\"{value}\" WHERE id={self.get_id()}")
        conn.commit()

    def get_price(self):
        return self.__clist()[2]

    def set_price(self, value):
        c.execute(f"UPDATE items SET price={value} WHERE id={self.get_id()}")
        conn.commit()

    def get_cat_id(self):
        return self.__clist()[3]

    def set_cat_id(self, value):
        c.execute(f"UPDATE items SET cat_id={value} WHERE id={self.get_id()}")
        conn.commit()

    def get_desc(self):
        return self.__clist()[4]

    def set_desc(self, value):
        c.execute(f"UPDATE items SET desc=\"{value}\" WHERE id={self.get_id()}")
        conn.commit()

    def is_active(self):
        return self.__clist()[5] == 1

    def set_active(self, value):
        c.execute(f"UPDATE items SET active={value} WHERE id={self.get_id()}")
        conn.commit()

    def get_amount(self):
        return int(self.__clist()[6])
    
    def set_amount(self, value):
        c.execute(f"UPDATE items SET amount={value} WHERE id={self.get_id()}")
        conn.commit()

    def delete(self):
        c.execute(f"DELETE FROM items WHERE id={self.get_id()}")
        conn.commit()


def get_item_list():
    c.execute("SELECT * FROM items")
    return map(Item, [item[0] for item in list(c)])


def create_item(name, price, cat_id, desc):
    c.execute(f"INSERT INTO items(name, price, cat_id, desc, active, amount) VALUES(?, ?, ?, ?, 1, 0)", [name, price, cat_id, desc])
    conn.commit()


class Category:
    def __init__(self, cat_id):
        self.id = cat_id

    def get_id(self):
        return self.id

    def __clist(self):
        c.execute(f"SELECT * FROM cats WHERE id={self.get_id()}")
        return list(c)[0]

    def get_name(self):
        return self.__clist()[1]

    def set_name(self, value):
        c.execute(f"UPDATE cats SET name=\"{value}\" WHERE id={self.get_id()}")
        conn.commit()

    def delete(self):
        c.execute(f"DELETE FROM cats WHERE id={self.get_id()}")
        conn.commit()

    def get_item_list(self):
        c.execute(f"SELECT * FROM items WHERE cat_id={self.get_id()}")
        return map(Item, [item[0] for item in list(c)])


def get_cat_list():
    c.execute(f"SELECT * FROM cats")
    return map(Category, [cat[0] for cat in list(c)])
    

def create_cat(cat_name):
    c.execute(f"INSERT INTO cats(name) VALUES(?)", [cat_name])
    conn.commit()


class Order:
    def __init__(self, id):
        self.id = id
    
    def get_order_id(self):
        return self.id
    
    def __clist(self):
        c.execute(f"SELECT * FROM orders WHERE order_id=?", [self.get_order_id()])
        return list(c)[0]
    
    def get_user_id(self):
        return self.__clist()[1]
    
    def get_item_list(self):
        return list(map(Item, [item_id for item_id in self.__clist()[2].split(",")]))
    
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
        return self.__clist()[7]
    
    # Order status codes:
    # 0 - Processing
    # 1 - Delievery
    # 2 - Done
    # -1 - Canceled
    
    def get_status(self):
        return self.__clist()[8]
    
    def set_status(self, value):
        c.execute(f"UPDATE orders SET status=? WHERE order_id=?", [value, self.get_order_id()])
        conn.commit()
    
def does_order_exist(order_id):
    c.execute(f"SELECT * FROM orders WHERE order_id=?", [order_id])
    return len(list(c)) == 1
    
def create_order(order_id, user_id, item_list, email_adress, additional_message, phone_number="None", home_adress="None"):
    c.execute(f"INSERT INTO orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", [order_id, user_id, item_list, email_adress, phone_number, home_adress, additional_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0])
    conn.commit()
    return Order(order_id)