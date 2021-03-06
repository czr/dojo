import unittest
import sys

from basket import \
    generate_combinations, \
    calculate_price, \
    calculate_possible_discounts, \
    calculate_discount_two_for_one, \
    calculate_discount_three_for_two, \
    calculate_discount_five_for_three, \
    Basket

from pprint import pprint


class BasketTest(unittest.TestCase):

    def test_empty_basket(self):
        basket = Basket()
        print(basket.items)
        price_list = {}
        price = calculate_price(basket, price_list, [])
        self.assertEqual(price, 0)

    def test_one_item(self):
        basket = Basket({'ItemA': 1})
        price_list = { 'ItemA': 5 }
        price = calculate_price(basket, price_list, [])
        self.assertEqual(price, 5)

    def test_two_items(self):
        basket = Basket({'ItemA': 1, 'ItemB': 1})
        price_list = { 'ItemA': 5, 'ItemB': 1 }
        price = calculate_price(basket, price_list, [])
        self.assertEqual(price, 6)

    def test_repeated_items(self):
        basket = Basket({'ItemA': 2})
        price_list = { 'ItemA': 5 }
        price = calculate_price(basket, price_list, [])
        self.assertEqual(price, 10)

    def test_weighed_item(self):
        basket = Basket({'WeighedItemA': 3})
        price_list = { 'WeighedItemA': 5 }
        price = calculate_price(basket, price_list, [])
        self.assertEqual(price, 15)

    def test_bogof_with_one(self):
        basket = Basket({'ItemA': 1})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_two_for_one]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 5)

    def test_bogof_with_two(self):
        basket = Basket({'ItemA': 2})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_two_for_one]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 5)

    def test_bogof_with_three(self):
        basket = Basket({'ItemA': 3})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_two_for_one]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 10)

    def test_three_for_two_with_three(self):
        basket = Basket({'ItemA': 3})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_three_for_two]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 10)

    def test_five_for_three_with_five(self):
        basket = Basket({'ItemA': 5})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_five_for_three]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 15)

    def test_generate_combinations_single(self):
        combinations = generate_combinations(['ItemA'], 3)
        self.assertItemsEqual(combinations, [['ItemA', 'ItemA', 'ItemA']])

    def test_generate_combinations_three(self):
        combinations = generate_combinations(['ItemA', 'ItemB', 'ItemC'], 1)
        self.assertItemsEqual(combinations, [
                ['ItemA'],
                ['ItemB'],
                ['ItemC'],
            ]
        )

    def test_discount_function(self):
        basket = Basket({'ItemA': 2})
        price_list = { 'ItemA': 5 }
        results = calculate_discount_two_for_one(basket, price_list)
        expected = [
            { 'basket': Basket(), 'discount': 5 },
        ]
        pprint(expected)
        self.assertEqual(results, expected)

    def test_discount_function_multiple_items(self):
        basket = Basket({'ItemA': 2, 'ItemB': 1})
        price_list = { 'ItemA': 5, 'ItemB': 4 }
        results = calculate_discount_two_for_one(basket, price_list)
        expected = [
            { 'basket': Basket({'ItemB': 1}), 'discount': 5 },
            { 'basket': Basket({'ItemA': 1}), 'discount': 5 },
            { 'basket': Basket({'ItemA': 1}), 'discount': 4 },
        ]

        self.assertItemsEqual(results, expected)

    def test_discount_function_multiple_items_in_discount(self):
        basket = Basket({'ItemA': 2, 'ItemB': 3})
        price_list = { 'ItemA': 5, 'ItemB': 4 }
        results = calculate_discount_five_for_three(basket, price_list)
        expected = [
            { 'basket': Basket({}), 'discount': 10 },
            { 'basket': Basket({}), 'discount': 9 },
            { 'basket': Basket({}), 'discount': 8 },
        ]
        self.assertItemsEqual(results, expected)

    def test_calculate_discounts_multiple(self):
        basket = Basket({'ItemA': 2, 'ItemB': 3})
        price_list = { 'ItemA': 5, 'ItemB': 4 }
        offers_list = [calculate_discount_five_for_three]
        results = calculate_possible_discounts(
            0,
            basket,
            price_list,
            offers_list
        )
        expected = [ 0, 10, 9, 8 ]
        self.assertItemsEqual(results, expected)

    # TODO - pull applies_to out of calculate_x_for_y
    def test_competing_offers(self):
        basket = Basket({'ItemA': 8})
        price_list = { 'ItemA': 5 }
        offers_list = [calculate_discount_three_for_two,
                       calculate_discount_five_for_three]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 25)

    def test_applying_offer_twice(self):
        basket = Basket({'ItemA': 4})
        price_list = {'ItemA': 5}
        offers_list = [calculate_discount_two_for_one]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 10)

    def test_calculate_possible_discounts_deep_recursion(self):
        basket = Basket({'ItemA': 40000})
        price_list = {'ItemA': 5}
        offers_list = [calculate_discount_two_for_one]
        price = calculate_price(basket, price_list, offers_list)
        self.assertEqual(price, 100000)


    # def test_offer_permutations(self):
    #     basket = Basket({'ItemA': 2, 'ItemB': 1})
    #     price_list = {'ItemA': 5, 'ItemB': 4}
    #     offers_list = [calculate_discount_two_for_one]
    #     price = calculate_price(basket, price_list, offers_list)
    #     self.assertEqual(price, 10)

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
