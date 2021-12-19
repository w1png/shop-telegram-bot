from aiogram import types
from aiogram.types.callback_query import CallbackQuery
from configparser import ConfigParser

import user as usr
import text_templates as tt
import item

conf = ConfigParser()
conf.read('config.ini', encoding='utf8')

# Назад
btnCatBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backCat')
btnFAQBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='goBackFaq')
btnOrdersBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='orders')
btnProfileBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backProfile')

goBackSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='botSettings')
goBackSettingsDel = types.InlineKeyboardButton(text="🔙Назад", callback_data="botSettingsDel")
goBackStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='shopStats')
goBackItems = types.InlineKeyboardButton(text='🔙Назад', callback_data='itemManagement')
goBackUserStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='userStatsBack')
goBackOrderStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='orderStatsBack')
goBackFromItem = types.InlineKeyboardButton(text='🔙Назад', callback_data='backFromitem')
btnCancelStateMainSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateMainSettings')
btnCancelStateQiwiSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateQiwiSettings')
btnCancelStateBTCSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateBTCSettings')
btnCancelStateClients = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateClients')
btnCancelStateItems = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateItems')
btnClientsBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='clientManagement')
btnCatsEditBack = types.InlineKeyboardButton(text="🔙Назад", callback_data="editCats")
btnStatsSettingsBack = types.InlineKeyboardButton(text="🔙Назад", callback_data="statsSettingsBack")
btnAdminBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backAdmin')


def get_cancel_states_editItem(itemid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"cancelStatesEditItem{itemid}"))
    return markup

def cancel_states_addaccounts(catid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"cancelStatesAddAccounts{catid}"))
    return markup


def get_back_item_edit(itemid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"editItem{itemid}"))
    return markup


def get_cancel_states_additem():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateItems)
    return markup


def get_back_cats_edit():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCatsEditBack)
    return markup


def get_back_cat_edit(catid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"editCat{catid}"))
    return markup


def get_cancel_states_cats(catid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"cancelStateCat{catid}"))
    return markup

def get_clients_back_button():
    return btnClientsBack


def get_items_back():
    markup = types.InlineKeyboardMarkup()
    markup.add(goBackItems)
    return markup


def get_cancel_states_clients():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateClients)
    return markup


def get_cancel_states_items():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateItems)
    return markup


def get_cancel_states_btc_settings():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateBTCSettings)
    return markup


def get_cancel_states_main_settings():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateMainSettings)
    return markup


def get_cancel_states_qiwi_settings():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateQiwiSettings)
    return markup


def get_user_stats_back():
    userStatsMarkup = types.InlineKeyboardMarkup()
    userStatsMarkup.add(goBackUserStats)
    return userStatsMarkup


def get_order_stats_back():
    markup = types.InlineKeyboardMarkup()
    markup.add(goBackOrderStats)
    return markup














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

# Stats
btnBackShopStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_shopStats")
btnBackRegistratonStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_registrationStatsBack")
btnBackOrderStats = types.InlineKeyboardButton(text=tt.back, callback_data="admin_orderStatsBack")

# /start menu
btnBackFaq = types.InlineKeyboardButton(text=tt.back, callback_data="faq")
btnBackProfile = types.InlineKeyboardButton(text=tt.back, callback_data="profile")
btnBackCatalogue = types.InlineKeyboardButton(text=tt.back, callback_data="catalogue")
def btnBackViewCat(cat_id): return types.InlineKeyboardButton(text=tt.back, callback_data=f"viewCat{cat_id}")


# Single buttons
btnAdminPanel = types.KeyboardButton(tt.admin_panel)
btnSupportMenu = types.KeyboardButton(tt.support_menu)

def single_button(btn):
    markup = types.InlineKeyboardMarkup()
    markup.add(btn)
    return markup


# Markups
# /start buttons
def get_markup_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(tt.catalogue))
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

def get_markup_profile(user_id):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.my_orders, callback_data="myOrders"))
    markup.add(types.InlineKeyboardButton(text=tt.my_support_tickets, callback_data="mySupportTickets"))

    user = usr.User(user_id)
    if user.is_admin():
        markup.add(types.InlineKeyboardButton(text=tt.disable_notif if user.notif_on() else tt.enable_notif, callback_data="disableNotif" if user.notif_on() else "enableNotif"))
    return markup

def get_markup_myOrders(order_list):
    markup = types.InlineKeyboardMarkup()
    for order in order_list:
        markup.add(types.InlineKeyboardButton(text=f"[{order[0]}] {order[4]}", callback_data=f"seeMyOrder{order[0]}"))
    markup.add(btnBackProfile)
    return markup

# Catalogue
def get_markup_catalogue(cat_list):
    markup = types.InlineKeyboardMarkup()
    for cat in cat_list:
        markup.add(types.InlineKeyboardButton(text=cat.get_name(), callback_data=f"viewCat{cat.get_id()}"))
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

def get_markup_editItem(item):
    itemid = item.get_id()
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=tt.change_name, callback_data=f"admin_editItemName{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_desc, callback_data=f"admin_editItemDesc{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_price, callback_data=f"admin_editItemPrice{itemid}"))
    markup.add(types.InlineKeyboardButton(text=tt.change_item_cat, callback_data=f"admin_editItemCat{itemid}"))
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
    markup.add(types.InlineKeyboardButton(text=tt.change_balance, callback_data=f"admin_cangeUserBalance{user.get_id()}"))
    
    btnMakeUserAdmin = types.InlineKeyboardButton(text=tt.add_admin_role, callback_data="admin_makeUserAdmin")
    btnRemoveUserAdmin = types.InlineKeyboardButton(text=tt.remove_admin_role, callback_data="admin_removeUserAdmin")
    markup.add(btnRemoveUserAdmin if user.is_admin() else btnMakeUserAdmin)
    
    btnRemoveUserSupport = types.InlineKeyboardButton(text=tt.remove_support_role, callback_data=f"admin_removeUserSupport{user.get_id()}")
    btnMakeUserSupport = types.InlineKeyboardButton(text=tt.add_support_role, callback_data=f"admin_makeUserSupport{user.get_id()}")
    markup.add(btnRemoveUserSupport if user.is_admin() else btnMakeUserSupport)
    
    markup.add(btnBackUserManagement)
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
    markup.add(types.InlineKeyboardButton(text=tt.stats_settings, callback_data="admin_statsSettings"))
    markup.add(btnBackAdmin)
    return markup


# userStatsMarkup = types.InlineKeyboardMarkup()
# userStatsMarkup.add(types.InlineKeyboardButton(text='За всё время', callback_data='userStatsAllTime'))
# userStatsMarkup.add(types.InlineKeyboardButton(text='За месяц', callback_data='userStatsMonth'))
# userStatsMarkup.add(types.InlineKeyboardButton(text='За неделю', callback_data='userStatsWeek'))
# userStatsMarkup.add(types.InlineKeyboardButton(text='За день', callback_data='userStatsDay'))
# userStatsMarkup.add(goBackStats)

# orderStatsMarkup = types.InlineKeyboardMarkup()
# orderStatsMarkup.add(types.InlineKeyboardButton(text='За всё время', callback_data='orderStatsAllTime'))
# orderStatsMarkup.add(types.InlineKeyboardButton(text='За месяц', callback_data='orderStatsMonthly'))
# orderStatsMarkup.add(types.InlineKeyboardButton(text='За неделю', callback_data='orderStatsWeekly'))
# orderStatsMarkup.add(types.InlineKeyboardButton(text='За день', callback_data='orderStatsDaily'))
# orderStatsMarkup.add(goBackStats)




























# товар

# c цена

def get_cat_edit_markup(catid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Изменить название", callback_data=f"editNameCat{catid}"))
    markup.add(types.InlineKeyboardButton(text="❌Удалить", callback_data=f"deleteCat{catid}"))
    markup.add(types.InlineKeyboardButton(text='🔙Назад', callback_data="editCats"))
    return markup




# пополнение баланса
def get_balance_markup():
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')

    balanceMarkup = types.InlineKeyboardMarkup()
    if conf['payment_settings']['qiwi_isactive'] == '1':
        btnQiwi = types.InlineKeyboardButton(text='🥝Qiwi', callback_data='qiwi')
        balanceMarkup.add(btnQiwi)

    btnYoomoney = types.InlineKeyboardButton(text='☂️ЮMoney', callback_data='yoomoney')
    balanceMarkup.add(btnYoomoney)

    if conf['payment_settings']['btc_isactive'] == '1':
        btnBTC = types.InlineKeyboardButton(text='💹BTC', callback_data='btc')
        balanceMarkup.add(btnBTC)

    btnPromo = types.InlineKeyboardButton(text='🧾Промокод', callback_data='promocode')
    balanceMarkup.add(btnPromo)
    balanceMarkup.add(btnProfileBack)
    return balanceMarkup


# Профиль



# Управление пользователями
clientManagementMarkup = types.InlineKeyboardMarkup()
btnSeeUserProfile = types.InlineKeyboardButton(text="📁Профиль пользователя", callback_data='seeUserProfile')
btnNotifyAllUsers = types.InlineKeyboardButton(text='🔔Оповещение всем пользователям', callback_data='notifyAll')
clientManagementMarkup.add(btnSeeUserProfile)
clientManagementMarkup.add(btnNotifyAllUsers)
clientManagementMarkup.add(btnAdminBack)


def get_client_management_markup():
    return clientManagementMarkup





def get_cancel_states_user(userid):
    markup = types.InlineKeyboardMarkup()
    btnCancelStateUser = types.InlineKeyboardButton(text='🔙Назад', callback_data=f'cancelStateUser{userid}')
    markup.add(btnCancelStateUser)
    return markup


def get_back_user_btn(userid):
    return types.InlineKeyboardButton(text="🔙Назад", callback_data=f"userBack{userid}")


def get_back_user_markup(userid):
    markup = types.InlineKeyboardMarkup()
    markup.add(get_back_user_btn(userid))
    return markup


def get_back_user_orders_markup(userid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"seeUserOrders{userid}"))
    return markup



# Настройки бота



def get_settings_markup():
    return settingsMarkup


# Основные настройки
def get_main_settings_markup():
    conf = ConfigParser()
    conf.read('config.ini', encoding='utf8')
    mainSettingsMarkup = types.InlineKeyboardMarkup()
    btnShopName = types.InlineKeyboardButton(text=f"Название: {conf['shop_settings']['shop_name']}",
                                             callback_data='changeShopName')
    btnShopContacts = types.InlineKeyboardButton(text=f"Контакты: {conf['shop_settings']['shop_contacts']}",
                                                 callback_data='changeContacts')
    btnRefundPolicy = types.InlineKeyboardButton(text=f"Политика возварата: {conf['shop_settings']['refund_policy']}",
                                                 callback_data='changeRefund')
    mainSettingsMarkup.add(btnShopName)
    mainSettingsMarkup.add(btnShopContacts)
    mainSettingsMarkup.add(btnRefundPolicy)
    mainSettingsMarkup.add(goBackSettings)
    return mainSettingsMarkup


# настройки статистики
def get_stats_settings_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="🌈Цвет графика", callback_data="statsColor"))
    markup.add(types.InlineKeyboardButton(text="🔲Ширина обводки", callback_data="statsBorderWidth"))
    markup.add(types.InlineKeyboardButton(text="ℹ️Размер названия графика", callback_data="statsTitleFontSize"))
    markup.add(types.InlineKeyboardButton(text="↔️Размер текста для осей", callback_data="statsAxisFontSize"))
    markup.add(types.InlineKeyboardButton(text="🔢Размер текста для делений", callback_data="statsTicksFontSize"))
    markup.add(goBackSettingsDel)
    return markup

def get_stats_color_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="⬛️", callback_data="statsColorBlack"), types.InlineKeyboardButton(text="⬜️", callback_data="statsColorWhite"), types.InlineKeyboardButton(text="🟥", callback_data="statsColorRed"))
    markup.add(types.InlineKeyboardButton(text="🟨", callback_data="statsColorYellow"), types.InlineKeyboardButton(text="🟪", callback_data="statsColorPurple"), types.InlineKeyboardButton(text="🟦", callback_data="statsColorBlue"))
    markup.add(types.InlineKeyboardButton(text="🟧", callback_data="statsColorOrange"), types.InlineKeyboardButton(text="🟩", callback_data="statsColorGreen"), types.InlineKeyboardButton(text="🟫", callback_data="statsColorBrown"))
    markup.add(btnStatsSettingsBack)
    return markup

def get_stats_border_width_markup():
    conf = ConfigParser()
    conf.read("config.ini", encoding="utf-8")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=("⛔️" if int(conf["stats_settings"]["linewidth"]) == 0 else "➖"), callback_data=("none" if int(conf["stats_settings"]["linewidth"]) == 0 else "statsBorderWidthReduce")), types.InlineKeyboardButton(text=conf["stats_settings"]["linewidth"], callback_data="defaultBorderWidth"), types.InlineKeyboardButton(text="➕", callback_data="statsBorderWidthAdd"))
    markup.add(btnStatsSettingsBack)
    return markup

def get_stats_font_markup(confsetting, callback):
    conf = ConfigParser()
    conf.read("config.ini", encoding="utf-8")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text=("⛔️" if int(conf["stats_settings"][confsetting]) == 2 else "➖"), callback_data=("none" if int(conf["stats_settings"][confsetting]) == 2 else callback + "Reduce")), types.InlineKeyboardButton(text=conf["stats_settings"][confsetting], callback_data=f"defaultFont{confsetting}"), types.InlineKeyboardButton(text="➕", callback_data=callback + "Add"))
    markup.add(btnStatsSettingsBack)
    return markup


def get_qiwi_settings():
    qiwi_conf = ConfigParser()
    qiwi_conf.read("config.ini", encoding="utf-8")

    qiwiSettingsMarkup = types.InlineKeyboardMarkup()
    btnQiwiNumber = types.InlineKeyboardButton(text=f"Номер QIWI: {qiwi_conf['payment_settings']['qiwi_number']}",
                                               callback_data='changeQiwiNumber')
    btnQiwiToken = types.InlineKeyboardButton(text=f"Токен QIWI: {qiwi_conf['payment_settings']['qiwi_token']}",
                                              callback_data='changeQiwiToken')
    if qiwi_conf['payment_settings']['qiwi_isactive'] == '0':
        btnOnOffQiwi = types.InlineKeyboardButton(text='✅Включить способ оплаты', callback_data='qiwiOn')
    else:
        btnOnOffQiwi = types.InlineKeyboardButton(text='❌Выключить способ оплаты', callback_data='qiwiOff')

    qiwiSettingsMarkup.add(btnOnOffQiwi)
    qiwiSettingsMarkup.add(btnQiwiNumber)
    qiwiSettingsMarkup.add(btnQiwiToken)
    qiwiSettingsMarkup.add(goBackSettings)
    return qiwiSettingsMarkup


def get_btc_settings_markup():
    btc_conf = ConfigParser()
    btc_conf.read('config.ini', encoding='utf8')
    btcMarkup = types.InlineKeyboardMarkup()
    if btc_conf['payment_settings']['btc_isactive'] == '0':
        btnOnOffBtc = types.InlineKeyboardButton(text='✅Включить способ оплаты', callback_data='btcOn')
    else:
        btnOnOffBtc = types.InlineKeyboardButton(text='❌Выключить способ оплаты', callback_data='btcOff')

    btnMainBtcAdress = types.InlineKeyboardButton(text=f"Адрес кошелька: {btc_conf['payment_settings']['main_btc_adress']}",
                                                  callback_data='changeMainBtc')
    btcMarkup.add(btnOnOffBtc)
    btcMarkup.add(btnMainBtcAdress)
    btcMarkup.add(goBackSettings)
    return btcMarkup


def get_profile_back():
    return btnProfileBack


def get_orders_back():
    return btnOrdersBack


def get_faq_back():
    return btnFAQBack


def get_cat_back():
    return btnCatBack


# Покупка

def get_item_markup(item_id, cat_id):
    itemMarkup = types.InlineKeyboardMarkup()
    btnBuy = types.InlineKeyboardButton(text='🛍️Купить', callback_data=f'confirm{item_id}')
    btnBackItem = types.InlineKeyboardButton(text='🔙Назад', callback_data=f'cat{cat_id}')
    itemMarkup.add(btnBuy)
    itemMarkup.add(btnBackItem)
    return itemMarkup


def get_confirm_buy_markup(item_id):
    markupConfirmBuy = types.InlineKeyboardMarkup()
    btnBuyYes = types.InlineKeyboardButton(text='✅Да', callback_data=f'buy{item_id}')
    btnBuyNo = types.InlineKeyboardButton(text='❌Нет', callback_data=f'item{item_id}')
    markupConfirmBuy.add(btnBuyYes, btnBuyNo)
    return markupConfirmBuy
