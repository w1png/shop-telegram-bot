import pymorphy2
import item as itm

m = pymorphy2.MorphAnalyzer()

def get_normal_form(word):
    return m.parse(word)[0].normal_form
    

def pr(item):
    print(item)

def search_item(query):
    probabilities = dict()
    for item in itm.get_item_list():
        probabilities[item.get_id()] = 0
        keywords = list(map(get_normal_form, item.get_name().split() + item.get_desc().split()))
        print(keywords)
        print(list(map(get_normal_form, query.split())))
        for word in list(map(get_normal_form, query.split())):
            probabilities[item.get_id()] += keywords.count(word)
    return dict(filter(lambda item: item[1] != 0, dict(sorted(probabilities.items(), key=lambda item: item[1])).items()))

if __name__ == "__main__":
    print(search_item("телефон с большим экраном"))