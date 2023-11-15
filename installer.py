from os import system, name, remove, mkdir, rmdir, listdir, environ
from os.path import exists
from sys import argv

import sqlite3


def clearConsole():
    system("cls" if name in ("nt", "dos") else "clear")

def create_config(token, main_admin_id, config_path="config.ini"):
    DEFAULT_CONFIG_TEXT = f"""[main_settings]
token = {token}
mainadminid = {main_admin_id}
debug = 0

[shop_settings]
name = Название магазина
greeting = Добро пожаловать!
refundpolicy = Текст для вкладки "Политика возврата"
contacts = Текст для вкладки "Контакты"
enableimage = 1
enablesticker = 0
enablephonenumber = 0
enabledelivery = 0
delivery_price = 0.0
enablecaptcha = 1

[stats_settings]
barcolor = 3299ff
borderwidth = 1
titlefontsize = 20
axisfontsize = 12
tickfontsize = 8
"""
    with open(config_path, "w") as config:
        config.write(DEFAULT_CONFIG_TEXT)


CREATE_CATS_TEXT = """
CREATE TABLE "cats" (
	"id" INTEGER,
	"name" TEXT NOT NULL,
	PRIMARY KEY("id")
)
"""
CREATE_ITEMS_TEXT = """
CREATE TABLE "items" (
	"id" INTEGER,
	"name" TEXT NOT NULL,
	"price" FLOAT NOT NULL,
	"cat_id" INTEGER NOT NULL,
	"desc" TEXT,
	"active" INTEGER,
	"amount" INTEGER,
	"image_id" INTEGER,
    "hide_image" INTEGER,
	PRIMARY KEY("id")
)
"""
CREATE_ORDERS_TEXT = """
CREATE TABLE "orders" (
	"order_id" INTEGER,
	"user_id" INTEGER,
	"item_list" TEXT,
	"email_adress" TEXT,
	"phone_number" TEXT,
	"home_adress" TEXT,
	"additional_message" TEXT,
	"date" TEXT,
    "status" INTEGER
    )
"""
CREATE_USERS_TEXT = """
CREATE TABLE "users" (
	"user_id" INTEGER NOT NULL,
	"is_admin" INTEGER,
	"is_manager" INTEGER,
	"notification" INTEGER,
	"date_created" TEXT,
    "cart" TEXT, 
    "cart_delivery" INTEGER
)
"""
CREATE_COMMANDS_TEXT = """
CREATE TABLE "commands" (
    "id" INTEGER NOT NULL,
    "command" TEXT,
    "response" TEXT,
    PRIMARY KEY("id")
)
"""

def create_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute(CREATE_CATS_TEXT)
    c.execute(CREATE_ITEMS_TEXT)
    c.execute(CREATE_ORDERS_TEXT)
    c.execute(CREATE_USERS_TEXT)
    c.execute(CREATE_COMMANDS_TEXT)
    conn.commit()
    conn.close()    

def do_files_exist():
    return any(list(map(exists, ["config.ini", "images", "data.db"])))

if __name__ == "__main__":
    if "--nointeract" in argv:
        if do_files_exist():
            exit(0)

        token = environ.get("TELEGRAM_TOKEN")
        main_admin_id = environ.get("MAIN_ADMIN_ID")
        if token is None or main_admin_id is None:
            print("Не указаны переменные окружения TELEGRAM_TOKEN или MAIN_ADMIN_ID")
            exit(1)
        create_config(token, main_admin_id)

        create_db()
        [mkdir(name) for name in ["backups", "images"]]

        exit(0)


    clearConsole()
    if do_files_exist():
        while True:
            confirmation = input("Вы уверены, что хотите повторно запустить процесс установки? Все данные будут утеряны! (y/N) ")
            if confirmation.lower() in ["y", "yes", "n", "no", ""]:
                break
    else:
        confirmation = "y"


    if confirmation.lower() in ["y", "yes"]:
        print("Вы можете узнать как получить токен бота, перейдя по ссылке: https://youtu.be/fyISLEvzIec")
        token = input("Введите токен бота: ")
        print("Вы можете получить ваш ID, написав \"/start\" боту @userinfobot")
        main_admin_id = input("Введите ID главного администратора: ")
        if main_admin_id.isalnum():
            if exists("data.db"):
                remove("data.db")
                print("База данных была удалена.")
            create_db()
            print("База данных была создана.")
            if exists("config.ini"):
                remove("config.ini")
                print("Файл настроек был удален.")
            create_config(token, main_admin_id)
            print("Файл настроек был создан.")
            if exists("images"):
                for file in listdir("images"):
                    remove("images/" + file)
                rmdir("images")
                print("Папка \"images\" была удалена.")
            mkdir("images")
            print("Папка \"images\" была создана.")
            if exists("backups"):
                for folder in listdir("backups"):
                    for file in listdir("backups/" + folder):
                        remove(f"backups/{folder}/{file}")
                    rmdir(f"backups/{folder}")
                rmdir("backups")
                print("Папка \"backups\" была удалена.")
            mkdir("backups")
            print("Папка \"backups\" была создана.")
        else:
            print("Неверный ID главного администратора.")
    else:
        print("Установка была отменена.")


    input("Нажмите ENTER, чтобы продолжить...")
