import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()


def get_commands():
    return list(map(Command, [command[0] for command in list(c.execute("SELECT * FROM commands"))]))

def does_command_exist(command_id):
    c.execute("SELECT * FROM commands WHERE id=?", [command_id])

def create_command(command, response):
    c.execute("INSERT INTO commands(command, response) VALUES(?,?)", [command, response])
    conn.commit()


# TODO: rework the permission system and implement command permissions
class Command:
    def __init__(self, command_id):
        self.command_id = command_id

    def __repr__(self):
        return f"[{self.get_id()}] {self.get_command()}"

    def __clist(self):
        c.execute("SELECT * FROM commands WHERE id=?", [self.command_id])
        return list(c)[0]

    def get_id(self):
        return self.command_id

    def get_command(self):
        return self.__clist()[1]

    def get_response(self):
        return self.__clist()[2]

    def delete(self):
        c.execute("DELETE * FROM commands WHERE id=?", [self.command_id])
        conn.commit()


if __name__ == "__main__":
    # create_command("test", "response")

    for command in get_commands():
        print(command)
