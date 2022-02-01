import unittest
from random import randint
from .utils import *

import src.item as itm
import src.category as cat



class TestItem(unittest.TestCase):
    def setUp(self):
        self.test_data_random = {
            "name": get_random_string(10, 40),
            "price": get_random_float(100, 10000),
            "cat_id": randint(1, 100),
            "desc": get_random_string(10, 255),
        }
        self.item_random = itm.create_item(self.test_data_random["name"], self.test_data_random["price"], self.test_data_random["cat_id"], self.test_data_random["desc"], active=False)
        
        self.test_data = {
            "name": "Test Item Name",
            "price": 999.99,
            "cat_id": cat.get_cat_list()[0].get_id(),
            "desc": "Test Item's description here. Blah-blah-blah..."
        }
        self.item = itm.create_item(self.test_data["name"], self.test_data["price"], self.test_data["cat_id"], self.test_data["desc"], active=False)
        

    def tearDown(self):
        self.item.delete()

    def test_name(self):
        self.assertEqual(self.item_random.get_name(), self.test_data_random["name"])
        name_random = get_random_string(2, 20)
        self.item_random.set_name(name_random)
        self.test_data_random["name"] = name_random
        self.assertEqual(self.item_random.get_name(), self.test_data_random["name"])

        self.assertEqual(self.item.get_name(), self.test_data["name"])
        name = "New test Item name"
        self.item.set_name(name)
        self.test_data["name"] = name
        self.assertEqual(self.item.get_name(), self.test_data["name"])

    def test_price(self):
        self.assertEqual(self.item_random.get_price(), self.test_data_random["price"])
        price_random = get_random_float(10, 1000)
        self.item_random.set_price(price_random)
        self.test_data_random["price"] = price_random
        self.assertEqual(self.item_random.get_price(), self.test_data_random["price"])

        self.assertEqual(self.item.get_price(), self.test_data["price"])
        price = 123.12
        self.item.set_price(price)
        self.test_data["price"] = price
        self.assertEqual(self.item.get_price(), self.test_data["price"])

    def test_cat_id(self):
        self.assertEqual(self.item_random.get_cat_id(), self.test_data_random["cat_id"])
        cat_id_random = randint(1, 100)
        self.item_random.set_cat_id(cat_id_random)
        self.test_data_random["cat_id"] = cat_id_random
        self.assertEqual(self.item_random.get_cat_id(), self.test_data_random["cat_id"])

        self.assertEqual(self.item.get_cat_id(), self.test_data["cat_id"])
        cat_id = 2
        self.item.set_cat_id(cat_id)
        self.test_data["cat_id"] = cat_id
        self.assertEqual(self.item.get_cat_id(), self.test_data["cat_id"])
    
    def test_desc(self):
        self.assertEqual(self.item_random.get_desc(), self.test_data_random["desc"])
        desc_random = get_random_string(10, 255)
        self.item_random.set_desc(desc_random)
        self.test_data_random["desc"] = desc_random
        self.assertEqual(self.item_random.get_desc(), self.test_data_random["desc"])

        self.assertEqual(self.item.get_desc(), self.test_data["desc"])
        desc = "New desc"
        self.item.set_desc(desc)
        self.test_data["desc"] = desc
        self.assertEqual(self.item.get_desc(), self.test_data["desc"])

    def test_active(self):
        self.assertFalse(self.item.is_active())

        self.item.set_active(1)
        self.assertTrue(self.item.is_active())
        self.item.set_active(0)
        self.assertFalse(self.item.is_active())

    def test_amount(self):
        self.assertEqual(self.item_random.get_amount(), 0)
        amount_random = randint(1, 1000)
        self.item_random.set_amount(amount_random)
        self.test_data_random["amount"] = amount_random
        self.assertEqual(self.item_random.get_amount(), self.test_data_random["amount"])

        self.assertEqual(self.item.get_amount(), 0)
        amount = 90
        self.item.set_amount(amount)
        self.test_data["amount"] = amount
        self.assertEqual(self.item.get_amount(), self.test_data["amount"])

    # TODO: image test cases
    @unittest.SkipTest
    def test_get_image_id(self):
        pass

    @unittest.SkipTest
    def test_get_image(self):
        pass

    @unittest.SkipTest
    def test_set_image_id(self):
        pass

    def test_hide_image(self):
        self.assertFalse(self.item.is_hide_image())
        self.item.set_hide_image(1)
        self.assertTrue(self.item.is_hide_image())
        self.item.set_hide_image(0)
        self.assertFalse(self.item.is_hide_image())


if __name__ == "__main__":
    unittest.main()
