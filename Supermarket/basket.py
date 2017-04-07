def calculate_price(basket, price_list, offers):
    # offers_list = { 'ItemA': 'bogof' }
    price = 0

    print(basket.items)
    for item, quantity in basket.items.items():
        price += price_list[item] * quantity

    discount = calculate_discounts(basket, price_list, offers)

    return price - discount

def calculate_discounts(basket, price_list, offers):
    total_discount = 0

    calculated_discounts = []
    for offer in offers:
        possibilities = offer(basket, price_list)
        if possibilities:
            best_discount = possibilities[0]['discount']
            total_discount += best_discount

    return total_discount

def calculate_x_for_y(x, y, basket, price_list):
    applies_to = 'ItemA'
    items = basket.items
    if items.get(applies_to, 0) >= x:
        new_basket = Basket(items=basket.items.copy())
        new_basket.items[applies_to] -= x
        return [{
            'basket': new_basket,
            'discount': price_list[applies_to] * (x - y)
        }]
    else:
        return []

def calculate_discount_three_for_two(basket, price_list):
    return calculate_x_for_y(3, 2, basket, price_list)

def calculate_discount_five_for_three(basket, price_list):
    return calculate_x_for_y(5, 3, basket, price_list)

def calculate_discount_two_for_one(basket, price_list):
    return calculate_x_for_y(2, 1, basket, price_list)

class Basket(object):
    """docstring for Basket."""
    def __init__(self, items=None):
        super(Basket, self).__init__()
        self.items = {} if items is None else items

    def __cmp__(self, other):
        return self.items == other.items

    def add_item(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity
