from configparser import ConfigParser
from genericpath import exists
from os import remove
import sqlite3

class Settings:
    def __init__(self, config_path="config.ini"):
        self.__config_path = config_path

    def __get_config(self):
        conf = ConfigParser()
        conf.read(self.__config_path)
        return conf
    
    def __set_setting(self, category, subcategory, value):
        conf = self.__get_config()
        conf.set(category, subcategory, str(value))
        with open(self.__config_path, 'w') as config:
            conf.write(config)
    
    # main_settings
    def get_token(self):
        return self.__get_config()["main_settings"]["token"]
    
    def set_token(self, value):
        self.__set_setting("main_settings", "token", value)
        
    def is_debug(self):
        return self.__get_config()["main_settings"]["debug"] == "1"
        
    def set_debug(self, value):
        self.__set_setting("main_settings", "debug", value)
    
    def get_main_admin_id(self):
        return self.__get_config()["main_settings"]["mainadminid"]
    
    def set_main_admin_id(self, value):
        self.__set_setting("main_settings", "mainadminid", value)
    
    # shop_settings
    def get_shop_name(self):
        return self.__get_config()["shop_settings"]["name"]
    
    def set_shop_name(self, value):
        self.__set_setting("shop_settings", "name", value)
    
    def get_shop_greeting(self):
        return self.__get_config()["shop_settings"]["greeting"]
    
    def set_shop_greeting(self, value):
        self.__set_setting("shop_settings", "greeting", value)
    
    def is_sticker_enabled(self):
        return self.__get_config()["shop_settings"]["enablesticker"] == "1"
    
    def set_enable_sticker(self, value):
        self.__set_setting("shop_settings", "enablesticker", value)
    
    def get_refund_policy(self):
        return self.__get_config()["shop_settings"]["refundpolicy"]
    
    def set_refund_policy(self, value):
        self.__set_setting("shop_settings", "refundpolicy", value)
    
    def get_shop_contacts(self):
        return self.__get_config()["shop_settings"]["contacts"]
    
    def set_shop_contacts(self, value):
        self.__set_setting("shop_settings", "contacts", value)
    
    def is_item_image_enabled(self):
        return self.__get_config()["shop_settings"]["enableimage"] == "1"
    
    def set_item_image(self, value):
        self.__set_setting("shop_settings", "enableimage", value)    
        
    def is_phone_number_enabled(self):
        return self.__get_config()["shop_settings"]["enablephonenumber"] == "1"
    
    def set_enable_phone_number(self, value):
        self.__set_setting("shop_settings", "enablephonenumber", value)
        
    def is_delivery_enabled(self):
        return self.__get_config()["shop_settings"]["enabledelivery"] == "1"
    
    def set_delivery(self, value):
        self.__set_setting("shop_settings", "enabledelivery", value)
        
    def get_delivery_price(self):
        return float(self.__get_config()["shop_settings"]["delivery_price"])
    
    def set_delivery_price(self, value):
        self.__set_setting("shop_settings", "delivery_price", value)
        
    def is_captcha_enabled(self):
        return self.__get_config()["shop_settings"]["enablecaptcha"] == "1"
    
    def set_enable_captcha(self, value):
        self.__set_setting("shop_settings", "enablecaptcha", value)
        
    # stats_settings
    def get_barcolor(self):
        return self.__get_config()["stats_settings"]["barcolor"]
    
    def set_barcolor(self, value):
        self.__set_setting("stats_settings", "barcolor", value)
    
    def get_borderwidth(self):
        return self.__get_config()["stats_settings"]["borderwidth"]
    
    def set_borderwidth(self, value):
        self.__set_setting("stats_settings", "borderwidth", value)
    
    def get_titlefontsize(self):
        return self.__get_config()["stats_settings"]["titlefontsize"]
    
    def set_titlefontsize(self, value):
        self.__set_setting("stats_settings", "titlefontsize", value)
    
    def get_axisfontsize(self):
        return self.__get_config()["stats_settings"]["axisfontsize"]
    
    def set_axisfontsize(self, value):
        self.__set_setting("stats_settings", "axisfontsize", value)
    
    def get_tickfontsize(self):
        return self.__get_config()["stats_settings"]["tickfontsize"]
    
    def set_tickfontsize(self, value):
        self.__set_setting("stats_settings", "tickfontsize", value)
        
    def reset(self):
        DEFAULT_CONFIG_TEXT = f"""[main_settings]
token = {self.get_token()}
mainadminid = {self.get_main_admin_id()}
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
        if exists("config.ini"):
            remove("config.ini")
        with open("config.ini", "w") as config:
            config.write(DEFAULT_CONFIG_TEXT)
    
    def clean_db(self):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("DELETE FROM cats")
        c.execute("DELETE FROM items")
        c.execute("DELETE FROM orders")
        c.execute("DELETE FROM commands")
        conn.commit()
        conn.close()
