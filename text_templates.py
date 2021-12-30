import item as itm

line_separator = "➖➖➖➖➖➖➖➖➖➖"


# Multiple lines
def get_profile_template(user):
    return f"{line_separator}\n📝 id: {user.get_id()}\n📈 Кол-во заказов: {len(user.get_orders())}\n📅 Дата регистрации: {user.get_register_date()}\n{line_separator}"

def get_faq_template(shop_name):
    return f"{line_separator}\nℹ️ FAQ магазина {shop_name}\n{line_separator}"

def get_categories_template():
    return f"{line_separator}\n🛍️ Категории\n{line_separator}"

def get_category_was_created_successfuly(cat_name):
    return f"Категория {cat_name} была успешно создана."

def get_category_data(cat):
    return f"{line_separator}\nID: {cat.get_id()}\nНазвание: {cat.get_name()}\n{line_separator}"

def get_item_card(item=None, name=None, price=None, desc=None, amount=None):
    if item:
        name = item.get_name()
        price = item.get_price()
        desc = item.get_desc()
        amount = item.get_amount()
        
    return f"{line_separator}\n{name} - {'{:.2f}'.format(price)} руб.\nВ наличии: {amount} шт.\n{line_separator}\n{desc}"

# Single phrases
# /start
admin_panel = "🔴 Админ панель"
faq = "ℹ️ FAQ"
profile = "📁 Профиль"
catalogue = "🗄️ Каталог"
cart = "🛒 Козрина"
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

# Catalogue / Item
add_to_cart = "🛒 Добавить в корзину"

# Item management
add_cat = "🛍️ Добавить категорию"
add_item = "🗃️ Добавить товар"
edit_cat = "✏️ Редактировать категорию"
edit_item = "✏️ Редактировать товар"
change_name = "📋 Изменить название"
change_desc = "📝 Изменить описание"
change_price = "🏷️ Изменить цену"
change_item_cat = "🛍️ Изменить категорию"
change_stock = "📦 Изменить кол-во"
hide = "🙈 Скрыть"
show = "🐵Показать"
delete = "❌ Удалить"

# User management
user_profile = "📁Профиль пользователя"
notify_everyone = "🔔Оповещение всем пользователям"
orders = "📁 Заказы"
remove_admin_role = "🔴 Убрать роль администратора"
add_admin_role = "🔴 Сделать администратором"
remove_support_role = "☎️ Убрать роль оператора тех. поддержки"
add_support_role = "☎️ Сделать оператором тех. поддержки"

# Shop stats
registration_stats = "👥Статистика регистраций"
order_stats = "📦Статистика заказов"
all_time = "За всё время"
monthly = "За последние 30 дней"
weekly = "За последние 7 дней"
daily = "За последние 24 часа"

# Shop settings
main_settings = "🛠️ Основные настройки"
stats_settings = "📈 Настройки статистики"
graph_color = "🌈 Цвет графика"
border_width = "🔲 Ширина обводки"
title_font_size = "ℹ️ Размер названия графика"
axis_font_size = "↔️Размер текста для осей"
tick_font_size = "🔢Размер текста для делений"
unavailable = "⛔️"
minus = "➖"
plus = "➕"


# Misc buttons
back = "🔙 Назад"
confirm = "✅ Да"
deny = "❌ Нет"
error = "Произошла ошибка!"
