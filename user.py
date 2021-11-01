import sqlite3
conn = sqlite3.connect('data.db')
c = conn.cursor()


def does_user_exist(user_id):
    c.execute(f"SELECT * FROM users WHERE user_id=\"{user_id}\"")
    return len(list(c)) != 0


def get_user_orders(user_id):
    c.execute(f"SELECT * FROM orders WHERE user_id=\"{user_id}\"")
    return list(c)


class User:
    def __init__(self, user_id):
        self.user_id = user_id

    def get_id(self):
        return self.user_id

    def get_balance(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[1]

    def is_admin(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[2] == 1

    def set_admin(self, value):
        c.execute(f"UPDATE users SET is_admin={value} WHERE user_id={self.get_id()}")
        conn.commit()

    def is_supplier(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[3] == 1

    def set_supplier(self, value):
        c.execute(f"UPDATE users SET is_supplier={value} WHERE user_id={self.get_id()}")
        conn.commit()

    def is_support(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[4] == 1

    def set_support(self, value):
        c.execute(f"UPDATE users SET is_support={value} WHERE user_id={self.get_id()}")
        conn.commit()

    def get_register_date(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[-1]

    def notif_on(self):
        c.execute(f"SELECT * FROM users WHERE user_id={self.user_id}")
        for user in c:
            pass
        return user[5] == 1

    def enable_notif(self):
        c.execute(f"UPDATE users SET notification=1 WHERE user_id={self.user_id}")

    def disable_notif(self):
        c.execute(f"UPDATE users SET notification=0 WHERE user_id={self.user_id}")


def set_user_balance(user_id, price, add_value=False, remove_value=False, set_value=False):
    c.execute(f"SELECT * FROM users WHERE user_id={user_id}")
    for user in c:
        pass
    if set_value:
        c.execute(f"UPDATE users SET balance={price} WHERE user_id={user_id}")
    elif add_value:
        new_bal = user[1] + price
        c.execute(f"UPDATE users SET balance={new_bal} WHERE user_id={user_id}")
    elif remove_value:
        old_bal = user[1]
        new_bal = old_bal - price
        c.execute(f"UPDATE users SET balance={new_bal} WHERE user_id={user_id}")
    conn.commit()


def get_notif_list():
    c.execute(f"SELECT * FROM users WHERE notification=1")
    return list(c)


def get_user_orders(userid):
    c.execute(f"SELECT * FROM orders WHERE user_id={userid}")
    return list(c)


def get_user_login(message):
    return message.from_user.username


def get_user_list():
    c.execute("SELECT * FROM users")
    return list(c)

