line_separator = "➖➖➖➖➖➖➖➖➖➖"


# multiple lines
def get_profile_template(chatid, user_orders, user_balance, user_reg_date):
    return f"{line_separator}\n📝 id:{chatid}\n📈 Кол-во заказов: {len(user_orders)}\n💸 Баланс: {user_balance}руб.\n📅 Дата регистрации: {user_reg_date}"

def get_faq_template(shop_name):
    return f"{line_separator}\nℹ️ FAQ магазина {shop_name}\n{line_separator}"

def get_categories_template():
    return f"{line_separator}\n🛍️ Категории\n{line_separator}"




# single phrases
admin_panel = "🔴 Админ панель"
faq = "ℹ️ FAQ"
profile = "📁 Профиль"
catalogue = "🛒 Каталог"
support_menu = "☎ Меню тех. поддержки"

item_management = "📦 Управление товаром"
client_management = "🧍 Управление пользователями"
item_stats = "📈 Статистика магазина (BETA)"
bot_settings = "⚙ Настройки бота"

my_orders = "📂 Мои заказы"
my_support_tickets = "🙋 Мои тикеты в тех. поддержку"
enable_notif = "🔔Включить ововещения о кол-ве товара"
disable_notif = "🔕Выключить ововещения о кол-ве товара"

back = "🔙 Назад"
