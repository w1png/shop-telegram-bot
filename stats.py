import datetime
import matplotlib.pyplot as plt
import sqlite3
from random import randint
from configparser import ConfigParser

class RegistrationCharts:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()
        self.conf = ConfigParser()
        self.conf.read("config.ini", encoding="utf-8")

    def clist(self):
        self.c.execute("SELECT * FROM users")
        return list(self.c)

    def saveplot(self, data, filename, title):
        plt.autoscale()
        plt.figure(figsize=(10, 10))
        plt.title(title, fontsize=self.conf["stats_settings"]["titlefontsize"])
        plt.xlabel("Дата", fontsize=self.conf["stats_settings"]["axisfontsize"])
        plt.ylabel("Кол-во регистраций", fontsize=self.conf["stats_settings"]["axisfontsize"])
        plt.tick_params(labelsize=self.conf["stats_settings"]["ticksfontsize"]) 
        plt.bar(range(len(data)), list(data.values()), color="#" + self.conf["stats_settings"]["barcolor"], edgecolor="black", linewidth=self.conf["stats_settings"]["borderwidth"])
        plt.xticks(range(len(data)), list(data.keys()), rotation=90)
        plt.savefig(f'images/{filename}.png')
        plt.close()
        return open(f'images/{filename}.png', 'rb')

    # TODO: maybe remake
    def all_time(self):
        registrations = {datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date(): 0 for user in self.clist()}
        for user in self.clist():
            registrations[datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date()] += 1
        registrations = {f"{date.day:02}.{date.month:02}.{date.year}": registrations[date] for date in list(registrations.keys())} # reverse for better visuals
        return self.saveplot(registrations, "registrations_all_time", "Регистрации за все время")

    def monthly(self):
        registrations = {datetime.date.today() - datetime.timedelta(days=i): 0 for i in range(30)}
        for user in self.clist():
            date = datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date()
            if date in registrations:
                registrations[date] += 1
        registrations = {f"{date.day:02}.{date.month:02}": registrations[date] for date in list(registrations.keys())[::-1]}
        return self.saveplot(registrations, "registrations_monthly", "Регистрации за последние 30 дней")

    def weekly(self):
        registrations = {datetime.date.today() - datetime.timedelta(days=i): 0 for i in range(7)}
        for user in self.clist():
            date = datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date()
            if date in registrations:
                registrations[date] += 1
        registrations = {f"{date.day:02}.{date.month:02}": registrations[date] for date in list(registrations.keys())[::-1]}
        return self.saveplot(registrations, "registrations_weekly", "Регистрации за последние 7 дней")
    
    def daily(self):
        registrations = {hour: 0 for hour in range(datetime.datetime.now().hour + 1)}
        for user in self.clist():
            if datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date() == datetime.date.today():
                registrations[datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").hour] += 1
        registrations = {f"{hour:02}:00": registrations[hour] for hour in list(registrations.keys())}
        return self.saveplot(registrations, "registrations_daily", "Регистрации за сегодня")


class OrderCharts:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.c = self.conn.cursor()
        self.conf = ConfigParser()
        self.conf.read("config.ini", encoding="utf-8")

    def clist(self):
        self.c.execute("SELECT * FROM orders")
        return list(self.c)

    def saveplot(self, data, filename, title):
        plt.autoscale()
        plt.figure(figsize=(10, 10))
        plt.title(title, fontsize=self.conf["stats_settings"]["titlefontsize"])
        plt.xlabel("Дата", fontsize=self.conf["stats_settings"]["axisfontsize"])
        plt.ylabel("Кол-во заказов", fontsize=self.conf["stats_settings"]["axisfontsize"])
        plt.tick_params(labelsize=self.conf["stats_settings"]["ticksfontsize"]) 
        plt.bar(range(len(data)), list(data.values()), color="#" + self.conf["stats_settings"]["barcolor"], edgecolor="black", linewidth=self.conf["stats_settings"]["borderwidth"])
        plt.bar(range(len(data)), list(data.values()))
        plt.xticks(range(len(data)), list(data.keys()), rotation=90)
        plt.savefig(f'images/{filename}.png')
        plt.close()
        return open(f'images/{filename}.png', 'rb')

    # TODO: maybe remake
    def all_time(self):
        orders = {datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").date(): 0 for order in self.clist()}
        for order in self.clist():
            orders[datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").date()] += 1
        orders = {f"{date.day:02}.{date.month:02}.{date.year}": orders[date] for date in list(orders.keys())}
        return self.saveplot(orders, "orders_all_time", "Заказы за все время")

    def monthly(self):
        orders = {datetime.date.today() - datetime.timedelta(days=i): 0 for i in range(30)}
        for order in self.clist():
            date = datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").date()
            if date in orders:
                orders[date] += 1
        orders = {f"{date.day:02}.{date.month:02}": orders[date] for date in list(orders.keys())[::-1]}
        return self.saveplot(orders, "orders_monthly", "Заказы за последние 30 дней")

    def weekly(self):
        orders = {datetime.date.today() - datetime.timedelta(days=i): 0 for i in range(7)}
        for order in self.clist():
            date = datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").date()
            if date in orders:
                orders[date] += 1
        orders = {f"{date.day:02}.{date.month:02}": orders[date] for date in list(orders.keys())[::-1]}
        return self.saveplot(orders, "orders_weekly", "Заказы за последние 7 дней")
    
    def daily(self):
        orders = {hour: 0 for hour in range(datetime.datetime.now().hour + 1)}
        for order in self.clist():
            if datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").date() == datetime.date.today():
                orders[datetime.datetime.strptime(order[-1], "%Y-%m-%d %H:%M:%S").hour] += 1
        orders = {f"{hour:02}:00": orders[hour] for hour in list(orders.keys())}
        return self.saveplot(orders, "orders_daily", "Заказы за сегодня")


def get_random_graph():
    conf = ConfigParser()
    conf.read("config.ini", encoding="utf-8")

    plt.autoscale()
    plt.figure(figsize=(10, 10))
    plt.title("Название", fontsize=conf["stats_settings"]["titlefontsize"])
    plt.xlabel("Ось Х", fontsize=conf["stats_settings"]["axisfontsize"])
    plt.ylabel("Ось У", fontsize=conf["stats_settings"]["axisfontsize"])
    plt.tick_params(labelsize=conf["stats_settings"]["ticksfontsize"]) 
    data = {f"{randint(1, 30):02}.{randint(1, 12):02}.{randint(2010, 2030)}": randint(5, 100) for _ in range(randint(2, 30))}
    plt.bar(range(len(data)), list(data.values()), color="#" + conf["stats_settings"]["barcolor"], edgecolor="black", linewidth=conf["stats_settings"]["borderwidth"])
    plt.xticks(range(len(data)), list(data.keys()), rotation=90)
    plt.savefig(f'images/random_graph.png')
    plt.close()
    return open(f'images/random_graph.png', 'rb')
