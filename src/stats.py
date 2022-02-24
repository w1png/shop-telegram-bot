import datetime
import matplotlib.pyplot as plt
import order as ordr
import user as usr
from random import randint
from settings import Settings

settings = Settings()

def saveplot(data, title, ylabel):
    plt.autoscale()
    plt.figure(figsize=(10, 10))
    plt.title(title, fontsize=settings.get_titlefontsize())
    plt.xlabel("Дата", fontsize=settings.get_axisfontsize())
    plt.ylabel(ylabel, fontsize=settings.get_axisfontsize())
    plt.tick_params(labelsize=settings.get_tickfontsize()) 
    plt.bar(range(len(data)), list(data.values()), color="#" + settings.get_barcolor(), edgecolor="black", linewidth=settings.get_borderwidth())
    plt.xticks(range(len(data)), list(data.keys()), rotation=90)
    plt.savefig(f"images/stats.png")
    plt.close()
    return open(f"images/stats.png", "rb")


def get_random_data():
    return {f"{randint(1, 30):02}.{randint(1, 12):02}.{randint(2010, 2030)}": randint(5, 100) for _ in range(randint(2, 30))}


def get_random_graph():
    return saveplot(get_random_data(), "Название", "Ось Y")


class RegistrationCharts:
    def __init__(self):
        self.user_list = usr.get_user_list()

    def saveplot(self, data, title):
        return saveplot(data, title, "Количество регистраций")

    def all_time(self):
        return self.saveplot({f"{date.day:02}.{date.month:02}.{date.year}": [user.get_register_date().date() for user in self.user_list].count(date) for date in dict.fromkeys([user.get_register_date().date() for user in self.user_list])}, "Регистрации за все время")

    def last_x_days(self, days):
        return self.saveplot({f"{(datetime.date.today() - datetime.timedelta(days=i)).day:02}.{(datetime.date.today() - datetime.timedelta(days=i)).month:02}": len(list(filter(lambda user: user.get_register_date().date() == datetime.date.today() - datetime.timedelta(days=i), self.user_list))) for i in range(30, -1, -1)}, f"Регистрации за последние {days} дней")

    def last_x_hours(self, hours):
        return self.saveplot({f"{(datetime.datetime.today() - datetime.timedelta(hours=i)).hour:02}:00": len(list(filter(lambda user: user.get_register_date().hour == (datetime.datetime.now() - datetime.timedelta(hours=i)).hour and user.get_register_date() > datetime.datetime.now() - datetime.timedelta(hours=hours), self.user_list))) for i in range(hours, -1, -1)}, f"Регистрации за последние {hours} часов.")


class OrderCharts:
    def __init__(self):
        self.order_list = ordr.get_order_list()

    def saveplot(self, data, title):
        return saveplot(data, title, "Количество заказов")

    def all_time(self):
        return self.saveplot({f"{date.day:02}.{date.month:02}.{date.year}": [order.get_date().date() for order in self.order_list].count(date) for date in dict.fromkeys([order.get_date().date() for order in self.order_list])}, "Заказы за все время")

    def last_x_days(self, days):
        return self.saveplot({f"{(datetime.date.today() - datetime.timedelta(days=i)).day:02}.{(datetime.date.today() - datetime.timedelta(days=i)).month:02}": len(list(filter(lambda order: order.get_date().date() == datetime.date.today() - datetime.timedelta(days=i), self.order_list))) for i in range(days, -1, -1)}, f"Заказы за последние {days} дней")

    def last_x_hours(self, hours):
        return self.saveplot({f"{(datetime.datetime.today() - datetime.timedelta(hours=i)).hour:02}:00": len(list(filter(lambda order: order.get_date() > datetime.datetime.now() - datetime.timedelta(hours=hours) and order.get_date().hour == (datetime.datetime.today() - datetime.timedelta(hours=i)).hour, self.order_list))) for i in range(hours, -1, -1)}, "Заказы за сегодня" if hours == (datetime.datetime.now().hour + 1) else f"Заказы за последние {hours} часов.")
