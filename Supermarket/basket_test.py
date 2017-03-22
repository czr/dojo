import unittest

from basket import calculate_price, calculate_discount_two_for_one, Basket

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

    def test_five_for_three_with_five(self):
        basket = [
            ('ItemA', 1),
            ('ItemA', 1),
            ('ItemA', 1),
            ('ItemA', 1),
            ('ItemA', 1),
        ]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': 'five_for_three' }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 15)

    def test_multiple_offers(self):
        basket = [
            ('ItemA', 1),
            ('ItemA', 1),
        ]
        price_list = { 'ItemA': 5 }
        offers_list = { 'ItemA': [ 'bogof', 'bogof' ] }
        price = calculate_price(basket, price_list, offers_list = offers_list)
        self.assertEqual(price, 5)

    def test_discount_function(self):
        basket = Basket()
        basket.add_item('ItemA', 2)
        price_list = { 'ItemA': 5 }
        results = calculate_discount_two_for_one(basket, price_list)
        expected = [
            { 'basket': Basket(), 'discount': 5 },
        ]
        self.assertEqual(results, expected)

    # TODO
    # def test_competing_offers(self):
    #     basket = [
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #         ('ItemA', 1),
    #     ]
    #     price_list = { 'ItemA': 5 }
    #     offers_list = { 'ItemA': [ 'three_for_two', 'five_for_three' ] }
    #     price = calculate_price(basket, price_list, offers_list = offers_list)
    #     self.assertEqual(price, 25)

        # {
        #     bogof: [ ItemA, ItemB ]
        #     buy_x_get_y: [ ItemC, ItemD ]
        # }
        # ( ItemA, ItemB ) == price of just one of A or B
        # ( ItemA, ItemA ) == price of just one of A
        # ( ItemC, ItemD ) == price of C
        #
        # {
        #     bogof: [ ItemA ]
        #     bogof: [ ItemB ]
        # }
        # ( ItemA, ItemB ) == price of A + B
        # ( ItemA, ItemA ) == price of one of A
