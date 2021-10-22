import sqlite3
import datetime
import matplotlib.pyplot as plt
import matplotlib

conn = sqlite3.connect('data.db')
c = conn.cursor()


# Пользователи
def get_chart(alltime=False, month=False, week=False, day=False):
    c.execute(f"SELECT * FROM users")
    x = list()

    if alltime:
        for user in c:
            x.append(datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date())
        formatter = matplotlib.dates.DateFormatter('%d.%m.%Y')
        filename = 'user_all_time'

    elif month:
        diff = 30 * 24
        date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
        formatter = matplotlib.dates.DateFormatter('%d')
        for user in c:
            combined = datetime.datetime.combine(datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date(), datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").time())
            if combined > date_diff:
                x.append(combined)
        filename = 'user_month'

    elif day:
        diff = 24
        date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
        formatter = matplotlib.dates.DateFormatter('%H:%M:%S')
        for user in c:
            combined = datetime.datetime.combine(datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date(),
                                                 datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").time())
            if combined > date_diff:
                x.append(combined)
        filename = 'user_day'

    elif week:
        diff = 24 * 7
        date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
        formatter = matplotlib.dates.DateFormatter('%d %a')
        for user in c:
            combined = datetime.datetime.combine(datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").date(),
                                                 datetime.datetime.strptime(user[-1], "%Y-%m-%d %H:%M:%S").time())
            if combined > date_diff:
                x.append(combined)
        filename = 'user_week'

    if x:
        x = matplotlib.dates.date2num(x)

        figure = plt.figure()
        axes = figure.add_subplot(1, 1, 1)
        axes.xaxis.set_major_formatter(formatter)

        plt.hist(x)
        plt.savefig(f'images/{filename}.png')
        return open(f'images/{filename}.png', 'rb')


# Товар
def get_chart_item(item_id=None, alltime=False, month=False, week=False, day=False):

    x = list()

    if item_id != None:
        c.execute(f"SELECT * FROM orders WHERE item_id={item_id}")
        for item in c:
            x.append(datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").date())
        formatter = matplotlib.dates.DateFormatter('%d.%m.%Y')
        filename = 'single_item_all_time'
    else:
        c.execute(f"SELECT * FROM orders")
        if alltime:
            for item in c:
                x.append(datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").date())
            formatter = matplotlib.dates.DateFormatter('%d.%m.%Y')
            filename = 'item_all_time'

        elif month:
            diff = 30 * 24
            date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
            formatter = matplotlib.dates.DateFormatter('%d')
            for item in c:
                combined = datetime.datetime.combine(datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").date(), datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").time())
                if combined > date_diff:
                    x.append(combined)
            filename = 'item_month'

        elif day:
            diff = 24
            date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
            formatter = matplotlib.dates.DateFormatter('%H:%M:%S')
            for item in c:
                combined = datetime.datetime.combine(datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").date(),
                                                     datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").time())
                if combined > date_diff:
                    x.append(combined)
            filename = 'item_day'

        elif week:
            diff = 24 * 7
            date_diff = datetime.datetime.now() - datetime.timedelta(hours=diff)
            formatter = matplotlib.dates.DateFormatter('%d %a')
            for item in c:
                combined = datetime.datetime.combine(datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").date(),
                                                     datetime.datetime.strptime(item[-1], "%Y-%m-%d %H:%M:%S").time())
                if combined > date_diff:
                    x.append(combined)
            filename = 'item_week'

    x = matplotlib.dates.date2num(x)

    figure = plt.figure()
    axes = figure.add_subplot(1, 1, 1)
    axes.xaxis.set_major_formatter(formatter)

    plt.hist(x)
    plt.savefig(f'images/{filename}.png')
    return open(f'images/{filename}.png', 'rb')
