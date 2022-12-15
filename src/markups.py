from os import listdir
from aiogram import types
from datetime import datetime

import text_templates as tt
from settings import Settings
import commands

settings = Settings()

# Back buttons
# Misc
btnBackAdmin = types.InlineKeyboardButton(text=tt.back, callback_data="admin_adminPanel")

# Item management
btnBackItemManagement = types.InlineKeyboardButton(text=tt.back, callback_data="admin_itemManagement")
btnBackEditCatChooseCategory = types.InlineKeyboardButton(text=tt.back, callback_data="admin_editCatChooseCategory")
def btnBackEditCat(cat_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"admin_editCat{cat_id}")
btnBackEditItemChooseCategory = types.InlineKeyboardButton(text=tt.back, callback_data="admin_editItemChooseCategory")
def btnBackEditItemChooseItem(cat_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"admin_editItemChooseItem{cat_id}")
def btnBackEditItem(item_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"admin_editItem{item_id}")

# User management
btnBackUserManagement = types.InlineKeyboardButton(text=tt.back, callback_data="admin_userManagement")
def btnBackSeeUserProfile(user_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"admin_seeUserProfile{user_id}")
def btnBackSeeUserOrders(user_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"admin_seeUserOrders{user_id}")

# Stats
btnBackShopStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_shopStats")
btnBackRegistratonStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_registrationStatsBack")
btnBackOrderStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_orderStatsBack")

# Settings
btnBackShopSettingsDel = types.InlineKeyboardButton(text=tt.back, callback_data="admin_shopSettingsDel")
btnBackShopSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_shopSettings")
btnBackStatsSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_statsSettings")
btnBackMainSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_mainSettings")
btnBackCheckoutSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_checkoutSettings")
btnBackAdditionalSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_additionalSettings")
btnBackCustomCommands = types.InlineKeyboardButton(text=tt.back, callback_data="admin_customCommands")
btnBackSystemSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_systemSettings")
btnBackItemSettings = types.InlineKeyboardButton(text=tt.back, callback_data="admin_itemSettings")
btnBackBackups = types.InlineKeyboardButton(text=tt.back, callback_data="admin_backups")

# /start menu
btnBackFaq = types.InlineKeyboardButton(text=tt.back, callback_data="faq")
btnBackProfile = types.InlineKeyboardButton(text=tt.back, callback_data="profile")
btnBackMyOrder = types.InlineKeyboardButton(text=tt.back, callback_data="myOrders")
btnBackCatalogue = types.InlineKeyboardButton(text=tt.back, callback_data="catalogue")
def btnBackViewCat(cat_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"viewCat{cat_id}")
def btnBackViewItem(item_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"viewItem{item_id}")
btnBackCart = types.InlineKeyboardButton(text=tt.back, callback_data="cart")
btnBackCartDel = types.InlineKeyboardButton(text=tt.back, callback_data="cartDel")
btnBackOrders = types.InlineKeyboardButton(text=tt.back, callback_data="manager_orders")

# Single buttons
btnAdminPanel = types.KeyboardButton(tt.admin_panel)
btnOrders = types.KeyboardButton(tt.orders)

def single_button(btn):
    markup = types.InlineKeyboardMarkup()
    markup.add(btn)
    return markup


# Markups
# /start buttons
def get_markup_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(tt.catalogue))
    markup.add(types.KeyboardButton(tt.cart))
    markup.add(types.KeyboardButton(tt.profile), types.KeyboardButton(tt.faq))
    return markup

def get_markup_admin():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.item_management, callback_data="admin_itemManagement"))
    markup.add(types.InlineKeyboardButton(text=tt.user_management, callback_data="admin_userManagement"))
    markup.add(types.InlineKeyboardButton(text=tt.shop_stats, callback_data="admin_shopStats"))
    markup.add(types.InlineKeyboardButton(text=tt.bot_settings, callback_data="admin_shopSettings"))
    return markup

def get_markup_faq():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.contacts, callback_data="contacts"))
    markup.add(types.InlineKeyboardButton(text=tt.refund, callback_data="refund"))
    return markup

def get_markup_profile(user):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.my_orders, callback_data="myOrders"))
    # markup.add(types.InlineKeyboardButton(text=tt.my_support_tickets, callback_data="mySupportTickets"))
    if user.is_admin():
        markup.add(types.InlineKeyboardButton(text=tt.disable_notif if user.notif_on() else tt.enable_notif, callback_data="changeEnableNotif"))
    return markup

def get_markup_myOrders(order_list):
    markup = types.InlineKeyboardMarkup()
    for order in order_list:
        markup.add(types.InlineKeyboardButton(text=order.get_order_id(), callback_data=f"viewMyOrder{order.get_order_id()}"))
    markup.add(btnBackProfile)
    return markup

def get_markup_viewMyOrder(order):
    markup = types.InlineKeyboardMarkup()
    match order.get_status():
        case 0:
            markup.add(types.InlineKeyboardButton(text=tt.cancel_order, callback_data=f"cancelOrder{order.get_order_id()}"))
        case -1:
            markup.add(types.InlineKeyboardButton(text=tt.restore_order, callback_data=f"restoreOrder{order.get_order_id()}"))
    markup.add(btnBackMyOrder)
    return markup
def get_markup_cart(user):
    markup = types.InlineKeyboardMarkup()
    delivery_price = '{:.2f}'.format(float(settings.get_delivery_price()))
    for item_and_amount in user.get_cart_amount():
        markup.add(types.InlineKeyboardButton(text=f"{item_and_amount[0].get_name()[:30-len(f' - {item_and_amount[1]}шт.')-3]}... - {item_and_amount[1]}шт.", callback_data=f"viewItem{item_and_amount[0].get_id()}"))
        markup.add(types.InlineKeyboardButton(text=f"{item_and_amount[0].get_price() * item_and_amount[1]}руб.", callback_data="None"), types.InlineKeyboardButton(text=tt.plus, callback_data=f"addToCartFromCart{item_and_amount[0].get_id()}"), types.InlineKeyboardButton(text=tt.minus, callback_data=f"removeFromCartFromCart{item_and_amount[0].get_id()}"))
    if settings.is_delivery_enabled():
        markup.add(types.InlineKeyboardButton(text=tt.delivery_on(delivery_price) if user.is_cart_delivery() else tt.delivery_off(delivery_price), callback_data="changeCartDelivery"))
    else:
        markup.add(types.InlineKeyboardButton(text=tt.pickup, callback_data="None"))
        
    markup.add(types.InlineKeyboardButton(text=tt.clear_cart, callback_data="clearCart"))
    markup.add(types.InlineKeyboardButton(text=f"Всего: {'{:.2f}'.format(user.get_cart_price())}руб.", callback_data="None"))
    markup.add(types.InlineKeyboardButton(text=tt.cart_checkout, callback_data="checkoutCart"))   
    return markup

def get_markup_captcha():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Новая CAPTCHA", callback_data="refreshCaptcha"))
    markup.add(btnBackCartDel)
    return markup

def get_markup_checkoutCartConfirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.confirm, callback_data=f"checkoutCartConfirm"), types.InlineKeyboardButton(text=tt.deny, callback_data="cart"))
    return markup

# Catalogue
def get_markup_catalogue(cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=cat.get_name(), callback_data=f"viewCat{cat.get_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.search, callback_data="search"))
    return markup

def get_markup_search(query):
    markup = types.InlineKeyboardMarkup()
    for item in query:
        markup.add(types.InlineKeyboardButton(text=item.get_name(), callback_data=f"viewItem{item.get_id()}"))
    markup.add(btnBackCatalogue)
    return markup


def get_markup_viewCat(item_list):
    markup = types.InlineKeyboardMarkup()
    for item in item_list:
        if item.is_active():
            markup.add(types.InlineKeyboardButton(text=f"{item.get_name()} - {item.get_price()} руб.", callback_data=f"viewItem{item.get_id()}"))
    markup.add(btnBackCatalogue)
    return markup

def get_markup_viewItem(item):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.add_to_cart, callback_data=f"addToCart{item.get_id()}"))
    markup.add(btnBackViewCat(item.get_cat_id()))
    return markup

# Admin panel tabs
# Item management
def get_markup_itemManagement():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.add_cat, callback_data="admin_addCat"), types.InlineKeyboardButton(text=tt.add_item, callback_data="admin_addItem"))
    markup.add(types.InlineKeyboardButton(text=tt.edit_cat, callback_data="admin_editCatChooseCategory"), types.InlineKeyboardButton(text=tt.edit_item, callback_data="admin_editItemChooseCategory"))
    markup.add(btnBackAdmin)
    return markup

def get_markup_editCatChooseCategory(cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=f"[{cat.get_id()}] {cat.get_name()}", callback_data=f"admin_editCat{cat.get_id()}"))
    markup.add(btnBackItemManagement)
    return markup

def get_markup_editCat(cat_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.change_name, callback_data=f"admin_editCatName{cat_id}"))
    markup.add(types.InlineKeyboardButton(text=tt.delete, callback_data=f"admin_editCatDelete{cat_id}"))
    markup.add(btnBackEditCatChooseCategory)
    return markup

def get_markup_addItemSetCat(cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=f"[{cat.get_id()}] {cat.get_name()}", callback_data=f"admin_addItemSetCat{cat.get_id()}"))
    markup.add(btnBackItemManagement)    
    return markup

btnSkipAddItemSetImage = types.InlineKeyboardButton(text=tt.skip, callback_data="admin_skipSetAddItemSetImage")

def get_markup_addItemConfirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.confirm, callback_data="admin_addItemConfirm"), types.InlineKeyboardButton(text=tt.deny, callback_data="admin_itemManagement"))
    return markup

def get_markup_editItemChooseCategory(cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=f"[{cat.get_id()}] {cat.get_name()}", callback_data=f"admin_editItemChooseItem{cat.get_id()}"))
    markup.add(btnBackItemManagement)
    return markup

def get_markup_editItemChooseItem(item_list):
    markup = types.InlineKeyboardMarkup()
    for item in item_list:
        markup.add(types.InlineKeyboardButton(text=f"[{item.get_id()}] {item.get_name()}", callback_data=f"admin_editItem{item.get_id()}"))
    markup.add(btnBackEditItemChooseCategory)
    return markup

async def get_markup_editItem(item):
    itemid = item.get_id()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.change_name, callback_data=f"admin_editItemName{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_image, callback_data=f"admin_editItemImage{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.show_image if await item.is_hide_image() else tt.hide_image, callback_data=f"admin_editItemHideImage{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_desc, callback_data=f"admin_editItemDesc{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_price, callback_data=f"admin_editItemPrice{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_item_cat, callback_data=f"admin_editItemCat{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_stock, callback_data=f"admin_editItemStock{itemid}"))
    markup.add(types.InlineKeyboardButton(text=(tt.hide if item.is_active() else tt.show), callback_data=f"admin_editItemHide{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.delete, callback_data=f"admin_editItemDelete{itemid}"))
    markup.add(btnBackEditItemChooseItem(item.get_cat_id()))
    return markup

def get_markup_editItemCat(item_id, cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=f"[{cat.get_id()}] {cat.get_name()}", callback_data=f"admin_editItemSetCat{cat.get_id()}"))
    markup.add(btnBackEditItem(item_id))
    return markup

# User management
def get_markup_userManagement():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.user_profile, callback_data="admin_seeUserProfile"))
    markup.add(types.InlineKeyboardButton(text=tt.notify_everyone, callback_data="admin_notifyEveryone"))
    markup.add(btnBackAdmin)
    return markup

def get_markup_notifyEveryoneConfirmation():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.confirm, callback_data="admin_notifyEveryoneConfirm"), btnBackUserManagement)
    return markup

def get_markup_seeUserProfile(user):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.orders, callback_data=f"admin_seeUserOrders{user.get_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.remove_manager_role if user.is_manager() else tt.add_manager_role, callback_data=f"admin_changeUserManager{user.get_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.remove_admin_role if user.is_admin() else tt.add_admin_role, callback_data=f"admin_changeUserAdmin{user.get_id()}"))    
    markup.add(btnBackUserManagement)
    return markup

def get_markup_seeUserOrders(user):
    markup = types.InlineKeyboardMarkup()
    for order in user.get_orders():
        markup.add(types.InlineKeyboardButton(text=f"[{order.get_order_id()}]", callback_data=f"admin_seeUserOrder{order.get_order_id()}"))
    markup.add(btnBackSeeUserProfile(user.get_id()))
    return markup

def get_markup_seeUserOrder(order):
    markup = markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.processing), callback_data=f"admin_changeOrderStatusProcessing{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.delivery), callback_data=f"admin_changeOrderStatusDelivery{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.done), callback_data=f"admin_changeOrderStatusDone{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.cancelled), callback_data=f"admin_changeOrderStatusCancel{order.get_order_id()}"))
    markup.add(btnBackSeeUserOrders(order.get_user_id()))
    return markup

# Shop stats
def get_markup_shopStats():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.registration_stats, callback_data="admin_registrationStats"))
    markup.add(types.InlineKeyboardButton(text=tt.order_stats, callback_data="admin_orderStats"))
    markup.add(btnBackAdmin)
    return markup

def get_markup_registrationStats():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.all_time, callback_data="admin_registrationStatsAllTime"))
    markup.add(types.InlineKeyboardButton(text=tt.monthly, callback_data="admin_registrationStatsMonthly"))
    markup.add(types.InlineKeyboardButton(text=tt.weekly, callback_data="admin_registrationStatsWeekly"))
    markup.add(types.InlineKeyboardButton(text=tt.daily, callback_data="admin_registrationStatsDaily"))
    markup.add(btnBackShopStats)
    return markup

def get_markup_orderStats():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.all_time, callback_data="admin_orderStatsAllTime"))
    markup.add(types.InlineKeyboardButton(text=tt.monthly, callback_data="admin_orderStatsMonthly"))
    markup.add(types.InlineKeyboardButton(text=tt.weekly, callback_data="admin_orderStatsWeekly"))
    markup.add(types.InlineKeyboardButton(text=tt.daily, callback_data="admin_orderStatsDaily"))
    markup.add(btnBackShopStats)
    return markup

# Shop settings
def get_markup_shopSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.main_settings, callback_data="admin_mainSettings"))
    markup.add(types.InlineKeyboardButton(text=tt.item_settings, callback_data="admin_itemSettings"))
    markup.add(types.InlineKeyboardButton(text=tt.checkout_settings, callback_data="admin_checkoutSettings"))
    markup.add(types.InlineKeyboardButton(text=tt.stats_settings, callback_data="admin_statsSettings"))
    markup.add(types.InlineKeyboardButton(text=tt.additional_settings, callback_data="admin_additionalSettings"))
    markup.add(btnBackAdmin)
    return markup
    
def get_markup_mainSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=f"Название: {settings.get_shop_name()}", callback_data="admin_changeShopName"))
    markup.add(types.InlineKeyboardButton(text=f"Приветствие: {settings.get_shop_greeting()}", callback_data="admin_changeShopGreeting"))
    markup.add(types.InlineKeyboardButton(text=f"Политика возврата: {settings.get_refund_policy()}", callback_data="admin_changeShopRefundPolicy"))
    markup.add(types.InlineKeyboardButton(text=f"Контакты: {settings.get_shop_contacts()}", callback_data="admin_changeShopContacts"))
    markup.add(types.InlineKeyboardButton(text=tt.disable_sticker if settings.is_sticker_enabled() else tt.enable_sticker, callback_data="admin_changeEnableSticker"))
    markup.add(btnBackShopSettings)
    return markup

def get_markup_itemSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.disable_item_image if settings.is_item_image_enabled() else tt.enable_item_image, callback_data="admin_changeEnableItemImage"))
    markup.add(btnBackShopSettings)
    return markup

def get_markup_checkoutSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.delivery_price('{:.2f}'.format(settings.get_delivery_price())), callback_data="admin_changeDeliveryPrice"))
    markup.add(types.InlineKeyboardButton(text=tt.disable_delivery if settings.is_delivery_enabled() else tt.enable_delivery, callback_data="admin_changeEnableDelivery"))
    markup.add(types.InlineKeyboardButton(text=tt.disable_phone_number if settings.is_phone_number_enabled() else tt.enable_phone_number, callback_data="admin_changeEnablePhoneNumber"))
    markup.add(types.InlineKeyboardButton(text=tt.disable_captcha if settings.is_captcha_enabled() else tt.enable_captcha, callback_data="admin_changeEnableCaptcha"))
    markup.add(btnBackShopSettings)
    return markup

def get_markup_statsSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.graph_color, callback_data="admin_statsSettingsColor"))
    markup.add(types.InlineKeyboardButton(text=tt.border_width, callback_data="admin_statsSettingsBorderWidth"))
    markup.add(types.InlineKeyboardButton(text=tt.title_font_size, callback_data="admin_statsSettingsTitleFontSize"))
    markup.add(types.InlineKeyboardButton(text=tt.axis_font_size, callback_data="admin_statsSettingsAxisFontSize"))
    markup.add(types.InlineKeyboardButton(text=tt.tick_font_size, callback_data="admin_statsSettingsTickFontSize"))
    markup.add(btnBackShopSettingsDel)
    return markup

def get_markup_statsSettingsColor():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⬛️", callback_data="admin_statsSettingsColorBlack"), types.InlineKeyboardButton(text="⬜️", callback_data="admin_statsSettingsColorWhite"), types.InlineKeyboardButton(text="🟥", callback_data="admin_statsSettingsColorRed"))
    markup.add(types.InlineKeyboardButton(text="🟨", callback_data="admin_statsSettingsColorYellow"), types.InlineKeyboardButton(text="🟪", callback_data="admin_statsSettingsColorPurple"), types.InlineKeyboardButton(text="🟦", callback_data="admin_statsSettingsColorBlue"))
    markup.add(types.InlineKeyboardButton(text="🟧", callback_data="admin_statsSettingsColorOrange"), types.InlineKeyboardButton(text="🟩", callback_data="admin_statsSettingsColorGreen"), types.InlineKeyboardButton(text="🟫", callback_data="admin_statsSettingsColorBrown"))
    markup.add(btnBackStatsSettings)
    return markup

def get_markup_statsSettingsBorderWidth():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.unavailable if settings.get_borderwidth() == "0" else tt.minus, callback_data="None" if settings.get_borderwidth() == "0" else "admin_statsSettingsBorderWidthReduce"), types.InlineKeyboardButton(text=settings.get_borderwidth(), callback_data="admin_statsSettingsBorderWidthDefault"), types.InlineKeyboardButton(text=tt.plus, callback_data="admin_statsSettingsBorderWidthAdd"))
    markup.add(btnBackStatsSettings)
    return markup

def get_markup_statsSettingsTitleFontSize():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.unavailable if settings.get_titlefontsize() == "2" else tt.minus, callback_data="None" if settings.get_titlefontsize() == "2" else "admin_statsSettingsTitleFontSizeReduce"), types.InlineKeyboardButton(text=settings.get_titlefontsize(), callback_data="admin_statsSettingsTitleFontSizeDefault"), types.InlineKeyboardButton(text=tt.plus, callback_data="admin_statsSettingsTitleFontSizeAdd"))
    markup.add(btnBackStatsSettings)
    return markup

def get_markup_statsSettingsAxisFontSize():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.unavailable if settings.get_axisfontsize() == "2" else tt.minus, callback_data="None" if settings.get_axisfontsize() == "2" else "admin_statsSettingsAxisFontSizeReduce"), types.InlineKeyboardButton(text=settings.get_axisfontsize(), callback_data="admin_statsSettingsAxisFontSizeDefault"), types.InlineKeyboardButton(text=tt.plus, callback_data="admin_statsSettingsAxisFontSizeAdd"))
    markup.add(btnBackStatsSettings)
    return markup

def get_markup_statsSettingsTickFontSize():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.unavailable if settings.get_tickfontsize() == "2" else tt.minus, callback_data="None" if settings.get_tickfontsize() == "2" else "admin_statsSettingsTickFontSizeReduce"), types.InlineKeyboardButton(text=settings.get_tickfontsize(), callback_data="admin_statsSettingsTickFontSizeDefault"), types.InlineKeyboardButton(text=tt.plus, callback_data="admin_statsSettingsTickFontSizeAdd"))
    markup.add(btnBackStatsSettings)
    return markup

def get_markup_systemSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.clean_images, callback_data="admin_cleanImagesMenu"))
    markup.add(types.InlineKeyboardButton(text=tt.reset_settings, callback_data="admin_resetSettingsMenu"))
    markup.add(types.InlineKeyboardButton(text=tt.clean_database, callback_data="admin_cleanDatabaseMenu"))
    markup.add(types.InlineKeyboardButton(text=tt.backups, callback_data="admin_backups"))
    markup.add(types.InlineKeyboardButton(text=tt.disable_debug if settings.is_debug() else tt.enable_debug, callback_data="admin_changeEnableDebug"))
    markup.add(btnBackAdditionalSettings)
    return markup

def get_markup_backups():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.update_backup, callback_data="admin_updateBackup"))
    markup.add(types.InlineKeyboardButton(text=tt.load_backup, callback_data="admin_loadBackupMenu"))
    markup.add(types.InlineKeyboardButton(text=tt.clean_backups, callback_data="admin_cleanBackupsMenu"))
    markup.add(btnBackSystemSettings)
    return markup

def get_markup_loadBackupMenu():
    markup = types.InlineKeyboardMarkup()
    backups = listdir("backups")
    backups.sort(key=lambda b: datetime.strptime(b, "%d-%m-%Y"))
    for backup in backups[:90]:
        markup.add(types.InlineKeyboardButton(text=backup, callback_data=f"admin_loadBackup{backup}"))
    markup.add(btnBackBackups)
    return markup

def get_markup_cleanBackupsMenu():
    markup = types.InlineKeyboardMarkup()
    for days in ["7", "30", "90"]:
        markup.add(types.InlineKeyboardButton(text=f"{days} дней", callback_data=f"admin_cleanBackups{days}"))
    markup.add(types.InlineKeyboardButton(text="Удалить все резервные копии", callback_data="admin_cleanBackupsAll"))
    markup.add(btnBackBackups)
    return markup

def get_markup_cleanImagesMenu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.delete, callback_data="admin_cleanImages"))
    markup.add(btnBackSystemSettings)
    return markup

def get_markup_resetSettingsMenu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.reset, callback_data="admin_resetSettings"))
    markup.add(btnBackSystemSettings)
    return markup

def get_markup_cleanDatabaseMenu():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.delete, callback_data="admin_cleanDatabase"))
    markup.add(btnBackSystemSettings)
    return markup

# Manager tab
def get_markup_seeOrder(order, user_id=None):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.processing), callback_data=f"manager_changeOrderStatusProcessing{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.delivery), callback_data=f"manager_changeOrderStatusDelivery{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.done), callback_data=f"manager_changeOrderStatusDone{order.get_order_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_order_status(tt.cancelled), callback_data=f"manager_changeOrderStatusCancel{order.get_order_id()}"))
    markup.add(btnBackSeeUserOrders(user_id) if user_id else btnBackOrders)
    return markup

def get_markup_orders():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.processing, callback_data="manager_ordersProcessing"))
    markup.add(types.InlineKeyboardButton(text=tt.delivery, callback_data="manager_ordersDelivery"))
    markup.add(types.InlineKeyboardButton(text=tt.done, callback_data="manager_ordersDone"))
    markup.add(types.InlineKeyboardButton(text=tt.cancelled, callback_data="manager_ordersCancelled"))
    return markup

def get_markup_ordersByOrderList(order_list):
    markup = types.InlineKeyboardMarkup()
    for order in order_list:
        markup.add(types.InlineKeyboardButton(text=f"[{order.get_order_id()}]", callback_data=f"manager_seeOrder{order.get_order_id()}"))
    markup.add(btnBackOrders)
    return markup

def get_markup_additionalSettings():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.custom_commands, callback_data="admin_customCommands"))
    markup.add(types.InlineKeyboardButton(text=tt.system_settings, callback_data="admin_systemSettings"))
    markup.add(btnBackShopSettings)
    return markup

# Custom commands
def get_markup_customCommands():
    markup = types.InlineKeyboardMarkup()
    for command in commands.get_commands():
        markup.add(types.InlineKeyboardButton(text=command.get_command(), callback_data="None"), types.InlineKeyboardButton(text=tt.delete, callback_data=f"admin_deleteCommand{command.get_id()}"))
    markup.add(types.InlineKeyboardButton(text=tt.line_separator, callback_data="None"))
    markup.add(types.InlineKeyboardButton(text=tt.add_command, callback_data="admin_addCommand"))
    markup.add(btnBackAdditionalSettings)
    return markup
