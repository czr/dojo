import unittest

from basket import Basket

class BasketTest(unittest.TestCase):

    def test_empty_basket(self):
        basket = []
        price_list = {}
        price = Basket.calculate_price(basket, price_list)
        self.assertEqual(price, 0)

    def test_one_item(self):
        basket = [('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        price = Basket.calculate_price(basket, price_list)
        self.assertEqual(price, 5)

    def test_two_items(self):
        basket = [('ItemA', 1), ('ItemB', 1)]
        price_list = { 'ItemA': 5, 'ItemB': 1 }
        price = Basket.calculate_price(basket, price_list)
        self.assertEqual(price, 6)

    def test_repeated_items(self):
        basket = [('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        price = Basket.calculate_price(basket, price_list)
        self.assertEqual(price, 10)

    def test_weighed_item(self):
        basket = [('WeighedItemA', 3)]
        price_list = { 'WeighedItemA': 5 }
        price = Basket.calculate_price(basket, price_list)
        self.assertEqual(price, 15)

    def test_bogof(self):
        basket = [('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'bogof' }
        price = Basket.calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 5)
