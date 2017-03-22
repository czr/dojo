def calculate_discounts(basket, offers_list, price_list):
    quantities = {}
    for item in basket:
        quantities[item[0]] = quantities.get(item[0],0) + item[1]

    total_discount = 0
    for item, quantity in quantities.items():
        if item in offers_list:
            offers = offers_list[item]
            if type(offers) is not list:
                offers = [offers]
            best_discount = 0
            for offer in offers:
                discount_function = DISCOUNTS[offer]
                discount, participating_items_count = discount_function(quantity, price_list[item])
                if discount > best_discount:
                    best_discount = discount
            total_discount += best_discount

    return total_discount

def calculate_x_for_y(x, y, quantity, price):
    participating_items_count = (quantity / x) * (x - y)
    return (participating_items_count * price, participating_items_count)

def calculate_discount_bogof(quantity, price):
    return calculate_x_for_y(2, 1, quantity, price)

def calculate_discount_three_for_two(quantity, price):
    return calculate_x_for_y(3, 2, quantity, price)

def calculate_discount_five_for_three(quantity, price):
    return calculate_x_for_y(5, 3, quantity, price)

def calculate_discount_two_for_one(basket, price_list):
    applies_to = 'ItemA'
    items = basket.items
    if applies_to in items and items[applies_to] >= 2:
        items[applies_to] = items[applies_to] - 2
        return [ { 'basket': basket, 'discount': price_list[applies_to] } ]
    else:
        return []

DISCOUNTS = {
    'bogof': calculate_discount_bogof,
    'three_for_two': calculate_discount_three_for_two,
    'five_for_three': calculate_discount_five_for_three,
}

def calculate_price(basket, price_list, offers_list = {}):
    # offers_list = { 'ItemA': 'bogof' }
    price = 0

    for item in basket:
        price += price_list[item[0]] * item[1]

    discount = calculate_discounts(basket, offers_list, price_list)

    return price - discount

class Basket(object):
    """docstring for Basket."""
    def __init__(self, items={}):
        super(Basket, self).__init__()
        self.items = items

    def __eq__(self, other):
        return self.items == other.items

    def add_item(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity

    def remove_item(self, name, quantity):
        pass
