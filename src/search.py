import pymorphy2
from pyparsing import opAssoc
import item as itm

m = pymorphy2.MorphAnalyzer()

excluded_words = ["без", "в", "для", "до", "за", "из", "к", "под", "а", "о", "над", "на", "о", "об", "от", "перед", "по", "под", "при", "про", "с", "у"]

def get_normal_forms(word):
    return set(p.normal_form for p in m.parse(word))
    

class Query:
    def __init__(self, results):
        self.results = results

    def __get_items(self):
        return list(map(itm.Item, self.results.keys()))[::-1][:90]

    def match(self):
        return self.__get_items()

    def price(self):
        return sorted(list(map(itm.Item, self.results.keys()))[::-1], key=lambda item: item.get_price())

    def popular(self):
        pass

# a match in a name is 3 points
# a match in a desc is 1 point
def search_item(query):
    points = dict()
    for item in itm.get_item_list():
        points[item.get_id()] = 0
        for word in list(filter(lambda word: word not in excluded_words, query.split())):
            for p in get_normal_forms(word):
                for word_title in item.get_name().split():
                    if p in get_normal_forms(word_title):
                        points[item.get_id()] += 3
                for word_title in item.get_desc().split():
                    if p in get_normal_forms(word_title):
                        points[item.get_id()] += 1
        if points[item.get_id()] == 0:
            points.pop(item.get_id())
    return Query(dict(sorted(points.items(), key=lambda item: item[1])))
