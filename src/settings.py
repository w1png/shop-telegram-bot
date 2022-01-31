from configparser import ConfigParser

class Settings:
    def __get_config(self, config_path="config.ini"):
        conf = ConfigParser()
        conf.read(config_path, encoding='utf8')
        return conf
    
    def __set_setting(self, category, subcategory, value):
        conf = self.__get_config()
        conf.set(category, subcategory, str(value))
        with open("config.ini", 'w') as config:
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
        