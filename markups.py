from aiogram import types
from aiogram.types.callback_query import CallbackQuery
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
btnClose = types.InlineKeyboardButton(text="❌Закрыть", callback_data="close")
btnCatsEditBack = types.InlineKeyboardButton(text="🔙Назад", callback_data="editCats")
btnStatsSettingsBack = types.InlineKeyboardButton(text="🔙Назад", callback_data="statsSettingsBack")


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

btnItemManagement = types.InlineKeyboardButton(text='📦Управление товаром', callback_data='itemManagement')
markupAdmin.add(btnItemManagement)
btnClientManagement = types.InlineKeyboardButton(text='🧍Управление пользователями', callback_data='clientManagement')
markupAdmin.add(btnClientManagement)
btnStats = types.InlineKeyboardButton(text='📈Статистика магазина (BETA)', callback_data='shopStats')
markupAdmin.add(btnStats)
btnBotSettings = types.InlineKeyboardButton(text='⚙Настройки бота', callback_data='botSettings')
markupAdmin.add(btnBotSettings)
markupAdmin.add(btnClose)


def get_admin_markup():
    return markupAdmin


# товар
markupItemManagement = types.InlineKeyboardMarkup()
btnAddCat = types.InlineKeyboardButton(text="🛍️Добавить категорию", callback_data="addCat")
btnAddItem = types.InlineKeyboardButton(text="🗃️Добавить товар", callback_data="addItem")
markupItemManagement.add(btnAddCat, btnAddItem)

btnEditCats = types.InlineKeyboardButton(text="✏️ Изменить категорию", callback_data="editCats")
btnEditItems = types.InlineKeyboardButton(text="✏️ Изменить товар", callback_data="editItems")
markupItemManagement.add(btnEditCats, btnEditItems)

markupItemManagement.add(btnAdminBack)

def get_item_management_markup():
    return markupItemManagement
# c цена

def get_cat_edit_markup(catid):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="Изменить название", callback_data=f"editNameCat{catid}"))
    markup.add(types.InlineKeyboardButton(text="❌Удалить", callback_data=f"deleteCat{catid}"))
    markup.add(types.InlineKeyboardButton(text='🔙Назад', callback_data="editCats"))
    return markup


def get_edit_item_markup(item):
    itemid = item[0]
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text="📋Изменить название", callback_data=f"editNameItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text="📝Изменить описание", callback_data=f"editDescItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text="🏷️Изменить цену", callback_data=f"editPriceItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text="🛍️Изменить категорию", callback_data=f"editCatItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text=("🙈Скрыть товар" if item[5] == 1 else "🐵Показать товар"), callback_data=f"hideItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text="❌Удалить", callback_data=f"deleteItem{itemid}"))
    markup.add(types.InlineKeyboardButton(text="🔙Назад", callback_data=f"editItemsCat{item[3]}"))
    return markup

# статистика
markupStats = types.InlineKeyboardMarkup()
markupStats.add(types.InlineKeyboardButton(text='👥Статистика регистраций', callback_data='userStats'))
markupStats.add(types.InlineKeyboardButton(text='📦Статистика заказов', callback_data='orderStats'))
markupStats.add(btnAdminBack)

userStatsMarkup = types.InlineKeyboardMarkup()
userStatsMarkup.add(types.InlineKeyboardButton(text='За всё время', callback_data='userStatsAllTime'))
userStatsMarkup.add(types.InlineKeyboardButton(text='За месяц', callback_data='userStatsMonth'))
userStatsMarkup.add(types.InlineKeyboardButton(text='За неделю', callback_data='userStatsWeek'))
userStatsMarkup.add(types.InlineKeyboardButton(text='За день', callback_data='userStatsDay'))
userStatsMarkup.add(goBackStats)

orderStatsMarkup = types.InlineKeyboardMarkup()
orderStatsMarkup.add(types.InlineKeyboardButton(text='За всё время', callback_data='orderStatsAllTime'))
orderStatsMarkup.add(types.InlineKeyboardButton(text='За месяц', callback_data='orderStatsMonthly'))
orderStatsMarkup.add(types.InlineKeyboardButton(text='За неделю', callback_data='orderStatsWeekly'))
orderStatsMarkup.add(types.InlineKeyboardButton(text='За день', callback_data='orderStatsDaily'))
orderStatsMarkup.add(goBackStats)


def get_stats_markup():
    return markupStats


def get_user_stats_markup():
    return userStatsMarkup


def get_order_stats_markup():
    return orderStatsMarkup


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


# Управление пользователями
clientManagementMarkup = types.InlineKeyboardMarkup()
btnSeeUserProfile = types.InlineKeyboardButton(text="📁Профиль пользователя", callback_data='seeUserProfile')
btnNotifyAllUsers = types.InlineKeyboardButton(text='🔔Оповещение всем пользователям', callback_data='notifyAll')
clientManagementMarkup.add(btnSeeUserProfile)
clientManagementMarkup.add(btnNotifyAllUsers)
clientManagementMarkup.add(btnAdminBack)


def get_client_management_markup():
    return clientManagementMarkup


def get_seeUserProfile_markup(userid):
    user = usr.User(userid)
    seeUserProfileMarkup = types.InlineKeyboardMarkup()
    btnSeeUserOrders = types.InlineKeyboardButton(text="📁Заказы", callback_data=f"seeUserOrders{userid}")
    btnChangeUserBalance = types.InlineKeyboardButton(text="💎Изменить баланс", callback_data=f"changeUserBalance{userid}")
    seeUserProfileMarkup.add(btnSeeUserOrders, btnChangeUserBalance)

    btnUserRemoveAdmin = types.InlineKeyboardButton(text="🔴Убрать роль администратора", callback_data=f"removeUserAdmin{userid}")
    btnUserMakeAdmin = types.InlineKeyboardButton(text="🔴Сделать администратором", callback_data=f"makeUserAdmin{userid}")
    seeUserProfileMarkup.add(btnUserRemoveAdmin) if user.is_admin() else seeUserProfileMarkup.add(btnUserMakeAdmin)
    
    btnUserRemoveSupport = types.InlineKeyboardButton(text="☎️Убрать роль оператора тех. поддержки", callback_data=f"removeUserSupport{userid}")
    btnUserMakeSupport = types.InlineKeyboardButton(text="☎️Сделать оператором тех. поддержки", callback_data=f"makeUserSupport{userid}")
    seeUserProfileMarkup.add(btnUserRemoveSupport) if user.is_support() else seeUserProfileMarkup.add(btnUserMakeSupport)
    
    seeUserProfileMarkup.add(btnClientsBack)
    return seeUserProfileMarkup


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
settingsMarkup = types.InlineKeyboardMarkup()

settingsMarkup.add(types.InlineKeyboardButton(text=f"🛠️Основные настройки", callback_data='mainSettings'))
settingsMarkup.add(types.InlineKeyboardButton(text=f"🥝Настройки QIWI кошелька", callback_data='qiwiSettings'))
settingsMarkup.add(types.InlineKeyboardButton(text=f"💵Настройки BTC кошелька", callback_data='btcSettings'))
settingsMarkup.add(types.InlineKeyboardButton(text="📈Настройки статистики", callback_data="statsSettings"))
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
