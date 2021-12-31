from configparser import ConfigParser

class Settings:
    def __get_config(self):
        conf = ConfigParser()
        conf.read('config.ini', encoding='utf8')
        return conf
    
    def set_setting(self, category, subcategory, value):
        conf = self.__get_config()
        conf.set(category, subcategory, str(value))
        with open("config.ini", 'w') as config:
            conf.write(config)
    
    # main_settings
    def get_token(self):
        return self.__get_config()["main_settings"]["token"]
    
    def set_token(self, value):
        self.set_setting("main_settings", "token", value)
        
    def is_debug(self):
        return self.__get_config()["main_settings"]["debug"] == "True"
        
    def set_debug(self, value):
        self.set_setting("main_settings", "debug", value)
    
    def get_main_admin_id(self):
        return self.__get_config()["main_settings"]["mainadminid"]
    
    def set_main_admin_id(self, value):
        self.set_setting("main_settings", "mainadminid", value)
    
    # shop_settings
    def get_shop_name(self):
        return self.__get_config()["shop_settings"]["name"]
    
    def set_shop_name(self, value):
        self.set_setting("shop_settings", "name", value)
    
    def get_shop_greeting(self):
        return self.__get_config()["shop_settings"]["greeting"]
    
    def set_shop_greeting(self, value):
        self.set_setting("shop_settings", "greeting", value)
    
    def is_sticker_enabled(self):
        return self.__get_config()["shop_settings"]["enablesticker"] == "1"
    
    def set_sticker(self, value):
        self.set_setting("shop_settings", "enablesticker", value)
    
    def get_refund_policy(self):
        return self.__get_config()["shop_settings"]["refundpolicy"]
    
    def set_refund_policy(self, value):
        self.set_setting("shop_settings", "refundpolicy", value)
    
    def get_shop_contacts(self):
        return self.__get_config()["shop_settings"]["contacts"]
    
    def set_shop_contacts(self, value):
        self.set_setting("shop_settings", "contacts", value)
        
    def is_phone_number_enabled(self):
        return self.__get_config()["shop_settings"]["enablephonenumber"] == "1"
    
    def set_enable_phone_number(self, value):
        self.set_setting("shop_settings", "enablephonenumber", value)
        
    def is_home_adress_enabled(self):
        return self.__get_config()["shop_settings"]["enablehomeadress"] == "1"
    
    def set_enable_home_adress(self, value):
        self.set_setting("shop_settings", "enablehomeadress", value)
        
    def is_capcha_enabled(self):
        return self.__get_config()["shop_settings"]["enablecapcha"] == "1"
    
    def set_capcha(self, value):
        self.set_setting("shop_settings", "enablecapcha", value)
        
    # stats_settings
    def get_barcolor(self):
        return self.__get_config()["stats_settings"]["barcolor"]
    
    def set_barcolor(self, value):
        self.set_setting("stats_settings", "barcolor", value)
    
    def get_borderwidth(self):
        return self.__get_config()["stats_settings"]["borderwidth"]
    
    def set_borderwidth(self, value):
        self.set_setting("stats_settings", "borderwidth", value)
    
    def get_titlefontsize(self):
        return self.__get_config()["stats_settings"]["titlefontsize"]
    
    def set_titlefontsize(self, value):
        self.set_setting("stats_settings", "titlefontsize", value)
    
    def get_axisfontsize(self):
        return self.__get_config()["stats_settings"]["axisfontsize"]
    
    def set_axisfontsize(self, value):
        self.set_setting("stats_settings", "axisfontsize", value)
    
    def get_tickfontsize(self):
        return self.__get_config()["stats_settings"]["tickfontsize"]
    
    def set_tickfontsize(self, value):
        self.set_setting("stats_settings", "tickfontsize", value)
        
