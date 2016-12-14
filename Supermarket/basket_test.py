import unittest

from basket import calculate_price

class BasketTest(unittest.TestCase):

    def test_empty_basket(self):
        basket = []
        price_list = {}
        price = calculate_price(basket, price_list)
        self.assertEqual(price, 0)

    def test_one_item(self):
        basket = [('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        price = calculate_price(basket, price_list)
        self.assertEqual(price, 5)

    def test_two_items(self):
        basket = [('ItemA', 1), ('ItemB', 1)]
        price_list = { 'ItemA': 5, 'ItemB': 1 }
        price = calculate_price(basket, price_list)
        self.assertEqual(price, 6)

    def test_repeated_items(self):
        basket = [('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        price = calculate_price(basket, price_list)
        self.assertEqual(price, 10)

    def test_weighed_item(self):
        basket = [('WeighedItemA', 3)]
        price_list = { 'WeighedItemA': 5 }
        price = calculate_price(basket, price_list)
        self.assertEqual(price, 15)

    def test_bogof_with_one(self):
        basket = [('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'bogof' }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 5)

    def test_bogof_with_two(self):
        basket = [('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'bogof' }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 5)

    def test_bogof_with_three(self):
        basket = [('ItemA', 1), ('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'bogof' }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 10)

    def test_three_for_two_with_three(self):
        basket = [('ItemA', 1), ('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'three_for_two' }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 10)


    def test_competing_offers(self):
        basket = [('ItemA', 1), ('ItemA', 1)]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': [ 'bogof', 'three_for_two' ] }
        # price = calculate_price(backet, price_list, offers_list = offers_list)
        self.assertEqual(1,2);
