import item as itm

line_separator = "➖➖➖➖➖➖➖➖➖➖"


# Multiple lines
def get_profile_template(chatid, user_orders, user_balance, user_reg_date):
    return f"{line_separator}\n📝 id:{chatid}\n📈 Кол-во заказов: {len(user_orders)}\n💸 Баланс: {'{:.2f}'.format(user_balance)}руб.\n📅 Дата регистрации: {user_reg_date}\n{line_separator}"

def get_faq_template(shop_name):
    return f"{line_separator}\nℹ️ FAQ магазина {shop_name}\n{line_separator}"

def get_categories_template():
    return f"{line_separator}\n🛍️ Категории\n{line_separator}"

def get_category_was_created_successfuly(cat_name):
    return f"Категория {cat_name} была успешно создана."

def get_category_data(cat):
    return f"{line_separator}\nID: {cat.get_id()}\nНазвание: {cat.get_name()}\n{line_separator}"

def get_item_card(item=None, name=None, price=None, desc=None):
    if item:
        name = item.get_name()
        price = item.get_price()
        desc = item.get_desc()
    return f"{line_separator}\n{name} - {'{:.2f}'.format(price)} руб.\nВ наличии: {item.get_amount()} шт.\n{line_separator}\n{desc}"

# Single phrases
error = "Произошла ошибка!"

# /start
admin_panel = "🔴 Админ панель"
faq = "ℹ️ FAQ"
profile = "📁 Профиль"
catalogue = "🛒 Каталог"
support_menu = "☎ Меню тех. поддержки"

# Admin panel tabs
item_management = "📦 Управление товаром"
user_management = "🧍 Управление пользователями"
shop_stats = "📈 Статистика магазина (BETA)"
bot_settings = "⚙ Настройки бота"

# FAQ
contacts = "📞 Контакты"
refund = "🎫 Политика возврата"

# Profile
my_orders = "📂 Мои заказы"
my_support_tickets = "🙋 Мои тикеты в тех. поддержку"
enable_notif = "🔔Включить ововещения о кол-ве товара"
disable_notif = "🔕Выключить ововещения о кол-ве товара"

# Item management
add_cat = "🛍️ Добавить категорию"
add_item = "🗃️ Добавить товар"
edit_cat = "✏️ Редактировать категорию"
edit_item = "✏️ Редактировать товар"
change_name = "📋 Изменить название"
change_desc = "📝 Изменить описание"
change_price = "🏷️ Изменить цену"
change_item_cat = "🛍️ Изменить категорию"
change_supply = "📦 Изменить кол-во"
hide = "🙈 Скрыть"
show = "🐵Показать"
delete = "❌ Удалить"

# User management
user_profile = "📁Профиль пользователя"
notify_everyone = "🔔Оповещение всем пользователям"

# Shop stats
registration_stats = "👥Статистика регистраций"
order_stats = "📦Статистика заказов"

# Shop settings
main_settings = "🛠️Основные настройки"
stats_settings = "📈Настройки статистики"

# Misc buttons
back = "🔙 Назад"
confirm = "✅ Да"
deny = "❌ Нет"