from pprint import pprint

def calculate_price(basket, price_list, offers):
    # offers_list = { 'ItemA': 'bogof' }
    price = 0

    print(basket.items)
    for item, quantity in basket.items.items():
        price += price_list[item] * quantity

    discount = calculate_discounts(basket, price_list, offers)

    return price - discount

def calculate_discounts(basket, price_list, offers):
    # total_discount = 0

    # for offer in offers:
    #     possibilities = offer(basket, price_list)
    #     while possibilities:
    #         total_discount += possibilities[0]['discount']
    #         basket = possibilities[0]['basket']
    #         possibilities = offer(basket, price_list)

    discounts = [0]
    discounts.extend(calculate_possible_discounts(0, basket, price_list, offers))

    pprint(discounts)

    return max(discounts)

def calculate_possible_discounts(accumulated_discount, basket, price_list, offers):
    discounts = []

    for offer in offers:
        possibilities = offer(basket, price_list)
        if possibilities:
            discounts.append(accumulated_discount + possibilities[0]['discount'])
            discounts.extend(calculate_possible_discounts(
                accumulated_discount + possibilities[0]['discount'],
                possibilities[0]['basket'],
                price_list,
                offers))

    return discounts

def generate_combinations(items, quantity):
    if not items:
        raise Exception("generate_combinations called with empty items")

    if len(items) == 1:
        return set([
            hashabledict([
                (items[0], quantity)
            ])
        ])

    results = set()
    for i in range(0, quantity + 1):
        subitems = items[1:]
        for subset in generate_combinations(subitems, quantity - i):
            results.add(hashabledict(
                [(items[0], i)] + subset.items()
            ))

    return results

def calculate_x_for_y(x, y, basket, price_list):
    applies_to = ['ItemA', 'ItemB']
    combinations = generate_combinations(applies_to, x)
    #[(ItemA=3, ItemB=0), (ItemA=2, ItemB=1), (ItemA=1, ItemB=2), (etc...]

    # Iterate over combinations, see whether it fits the basket,
    # return discount if so. Combination fits basket if each item in
    # combination has at least that quantity in the basket.

    results = []

    for combination in combinations:
        try:
            new_basket = Basket(items=basket.items.copy())
            basket.remove_items(combination)
            for item in combination:
                results.append({
                    'basket': new_basket,
                    'discount': price_list[item] * (x - y)
                })
        except NotInBasketException:
            next

    return results

def calculate_discount_three_for_two(basket, price_list):
    return calculate_x_for_y(3, 2, basket, price_list)

def calculate_discount_five_for_three(basket, price_list):
    return calculate_x_for_y(5, 3, basket, price_list)

def calculate_discount_two_for_one(basket, price_list):
    return calculate_x_for_y(2, 1, basket, price_list)

class NotInBasketException(Exception):
    pass

class Basket(object):
    """docstring for Basket."""
    def __init__(self, items=None):
        super(Basket, self).__init__()
        self.items = {} if items is None else items

    def __cmp__(self, other):
        return cmp(self.items, other.items)

    def __repr__(self):
        return str(self.__dict__)

    def add_item(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity

    def remove_items(self, combination):
        for item, quantity in combination.items():
            self.remove_item(item, quantity)

    def remove_item(self, name, quantity):
        if quantity > 0:
            if self.items.get(name, 0) > quantity:
                self.items[name] -= quantity
                return
            if self.items.get(name, 0) == quantity:
                self.items.pop(name)
                return
            raise NotInBasketException(
                "Can't remove {} of {} from basket. Only {} in basket.".format(
                    quantity, name, self.items.get(name, 0)
                )
            )

class hashabledict(dict):
    def __hash__(self):
        return hash(tuple(sorted(self.items())))
