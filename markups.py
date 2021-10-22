from aiogram import types
import user as usr
from configparser import ConfigParser

conf = ConfigParser()
conf.read('config.ini', encoding='utf8')


# Назад
btnCatBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backCat')
btnFAQBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='goBackFaq')
btnOrdersBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='orders')
btnProfileBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backProfile')
btnAdminBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='backAdmin')
goBackSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='botSettings')
goBackStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='shopStats')
goBackUserStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='userStatsBack')
goBackOrderStats = types.InlineKeyboardButton(text='🔙Назад', callback_data='StatsItem')
goBackFromItem = types.InlineKeyboardButton(text='🔙Назад', callback_data='backFromitem')
goBackOrderStatsItem = types.InlineKeyboardButton(text='🔙Назад', callback_data='goBackOrderStatsItem')
btnCancelStateMainSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateMainSettings')
btnCancelStateQiwiSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateQiwiSettings')
btnCancelStateBTCSettings = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateBTCSettings')
btnCancelStateClients = types.InlineKeyboardButton(text='🔙Назад', callback_data='cancelStateClients')
btnClientsBack = types.InlineKeyboardButton(text='🔙Назад', callback_data='clientManagement')


def get_clients_back_button():
    return btnClientsBack


def get_cancel_states_clients():
    markup = types.InlineKeyboardMarkup()
    markup.add(btnCancelStateClients)
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


# Основное меню
markupMain = types.ReplyKeyboardMarkup(resize_keyboard=True)
profile = types.KeyboardButton('📁Профиль')
catalogue = types.KeyboardButton('🛒Каталог')
faq = types.KeyboardButton('ℹ️FAQ')
adminPanel = types.KeyboardButton('🔴Админ панель')
markupMain.row(catalogue)
markupMain.row(profile, faq)


def get_markup_main():
    return markupMain


# Админ-панель
markupAdmin = types.InlineKeyboardMarkup()

btnRolesManagement = types.InlineKeyboardButton(text='👨‍💻Управление ролями', callback_data='rolesManagement')
markupAdmin.add(btnRolesManagement)
btnItemManagement = types.InlineKeyboardButton(text='📦Управление товаром', callback_data='itemManagement')
markupAdmin.add(btnItemManagement)
btnClientManagement = types.InlineKeyboardButton(text='🧍Управление пользователями', callback_data='clientManagement')
markupAdmin.add(btnClientManagement)
btnStats = types.InlineKeyboardButton(text='📈Статистика магазина', callback_data='shopStats')
markupAdmin.add(btnStats)
btnBotSettings = types.InlineKeyboardButton(text='⚙Настройки бота', callback_data='botSettings')
markupAdmin.add(btnBotSettings)


def get_admin_markup():
    return markupAdmin


# статистика
markupStats = types.InlineKeyboardMarkup()
btnUserStats = types.InlineKeyboardButton(text='👥Статистика пользователей', callback_data='userStats')
markupStats.add(btnUserStats)
btnOrderStats = types.InlineKeyboardButton(text='📦Статистика заказов', callback_data='statsOrder')
markupStats.add(btnOrderStats)
markupStats.add(btnAdminBack)

userStats = types.InlineKeyboardMarkup()
btnUserStatsDay = types.InlineKeyboardButton(text='За день', callback_data='userStatsDay')
userStats.add(btnUserStatsDay)
btnUserStatsWeek = types.InlineKeyboardButton(text='За неделю', callback_data='userStatsWeek')
userStats.add(btnUserStatsWeek)
btnUserStatsMonth = types.InlineKeyboardButton(text='За месяц', callback_data='userStatsMonth')
userStats.add(btnUserStatsMonth)
btnUserStatsAllTime = types.InlineKeyboardButton(text='За всё время', callback_data='userStatsAllTime')
userStats.add(btnUserStatsAllTime)
userStats.add(goBackStats)


itemStatsMarkup = types.InlineKeyboardMarkup()
btnItemStatsDay = types.InlineKeyboardButton(text='За день', callback_data='StatsDayItem')
itemStatsMarkup.add(btnItemStatsDay)
btnItemStatsWeek = types.InlineKeyboardButton(text='За неделю', callback_data='StatsWeekItem')
itemStatsMarkup.add(btnItemStatsWeek)
btnItemStatsMonth = types.InlineKeyboardButton(text='За месяц', callback_data='StatsMonthItem')
itemStatsMarkup.add(btnItemStatsMonth)
btnItemStatsAllTime = types.InlineKeyboardButton(text='За всё время', callback_data='StatsAllTimeItem')
itemStatsMarkup.add(btnItemStatsAllTime)
itemStatsMarkup.add(goBackStats)


def get_stats_item_markup():
    return itemStatsMarkup


def get_stats_order_markup():
    statsOrderMarkup = types.InlineKeyboardMarkup()
    btnItemStats = types.InlineKeyboardButton(text='💡Статистика по товару', callback_data='StatsItem')
    statsOrderMarkup.add(btnItemStats)
    return statsOrderMarkup


def get_stats_markup():
    return markupStats


def get_user_stats_markup():
    return userStats


# FAQ панель
markupFAQ = types.InlineKeyboardMarkup()
btnRefund = types.InlineKeyboardButton(text='🎫Политика возврата', callback_data='refund')
btnContacts = types.InlineKeyboardButton(text='📞Контакты', callback_data='contacts')
markupFAQ.add(btnContacts)
markupFAQ.add(btnRefund)


def get_faq_markup():
    return markupFAQ


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
def get_markup_profile(user_id):
    markupProfile = types.InlineKeyboardMarkup()
    btnBalance = types.InlineKeyboardButton(text='💰Пополнить Баланс', callback_data='balance')
    btnOrders = types.InlineKeyboardButton(text='📂Мои заказы', callback_data='orders')
    btnSeeSupportTickets = types.InlineKeyboardButton(text='🙋Мои тикеты в тех. поддержку',
                                                      callback_data='seeSupportTickets')

    markupProfile.add(btnOrders)
    markupProfile.add(btnSeeSupportTickets)
    markupProfile.add(btnBalance)
    user = usr.User(user_id)

    if user.is_supplier() or user.is_admin():
        if user.notif_on():
            btnNotif = types.InlineKeyboardButton(text='🔕Выключить ововещения о кол-ве товара',
                                                  callback_data='disableNotif')
        else:
            btnNotif = types.InlineKeyboardButton(text='🔔Включить ововещения о кол-ве товара',
                                                  callback_data='enableNotif')
        markupProfile.add(btnNotif)
    return markupProfile


# Управление пользователей
clientManagementMarkup = types.InlineKeyboardMarkup()
btnSeeUserPurchases = types.InlineKeyboardButton(text='🛒Покупки пользователя', callback_data='seeUserPurchases')
btnAddBalance = types.InlineKeyboardButton(text='💎Изменить баланс', callback_data='addBal')
btnSeeOrder = types.InlineKeyboardButton(text='📂Посмотреть заказ', callback_data='seeOrder')
btnNotifyAllUsers = types.InlineKeyboardButton(text='🔔Оповещение всем пользователям', callback_data='notifyAll')
clientManagementMarkup.add(btnSeeUserPurchases, btnAddBalance)
clientManagementMarkup.add(btnSeeOrder)
clientManagementMarkup.add(btnNotifyAllUsers)
clientManagementMarkup.add(btnAdminBack)


def get_client_management_markup():
    return clientManagementMarkup



# Настройки бота
settingsMarkup = types.InlineKeyboardMarkup()
btnMainSettings = types.InlineKeyboardButton(text=f"🛠️Основные настройки", callback_data='mainSettings')
btnQiwiSettings = types.InlineKeyboardButton(text=f"🥝Настройки QIWI кошелька", callback_data='qiwiSettings')
btnBtcSettings = types.InlineKeyboardButton(text=f"💵Настройки BTC кошелька", callback_data='btcSettings')
settingsMarkup.add(btnMainSettings)
settingsMarkup.add(btnQiwiSettings)
settingsMarkup.add(btnBtcSettings)
settingsMarkup.add(btnAdminBack)


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


# Настройки qiwi
def get_qiwi_settings():
    qiwi_conf = ConfigParser()
    qiwi_conf.read('config.ini', encoding='utf8')

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
