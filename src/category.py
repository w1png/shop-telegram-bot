import sqlite3
import item as itm

conn = sqlite3.connect("data.db")
c = conn.cursor()

class Category:
    def __init__(self, cat_id):
        self.id = cat_id

    def __eq__(self, __o: object) -> bool:
        return self.get_id() == __o.get_id()

    def __repr__(self) -> str:
        return self.get_name()

    def get_id(self):
        return self.id

    def __clist(self):
        c.execute(f"SELECT * FROM cats WHERE id=?", [self.get_id()])
        return list(c)[0]

    def get_name(self):
        return self.__clist()[1]

    def set_name(self, value):
        c.execute(f"UPDATE cats SET name=? WHERE id=?", [value, self.get_id()])
        conn.commit()

    def delete(self):
        c.execute(f"DELETE FROM cats WHERE id=?", [self.get_id()])
        conn.commit()

    def get_item_list(self):
        c.execute(f"SELECT * FROM items WHERE cat_id=?", [self.get_id()])
        return list(map(itm.Item, [item[0] for item in list(c)]))


def get_cat_list():
    c.execute(f"SELECT * FROM cats")
    return list(map(Category, [cat[0] for cat in list(c)]))
    

def create_cat(cat_name):
    c.execute(f"INSERT INTO cats(name) VALUES(?)", [cat_name])
    conn.commit()


if __name__ == "__main__":
    print(get_cat_list())