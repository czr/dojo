import itertools

def calculate_price(basket, price_list, offers):
    # offers_list = { 'ItemA': 'bogof' }
    price = 0

    print(basket.items)
    for item, quantity in basket.items.items():
        price += price_list[item] * quantity

    discount = calculate_discounts(basket, price_list, offers)

    return price - discount


def calculate_discounts(basket, price_list, offers):
    discounts = [0]
    discounts.extend(
        calculate_possible_discounts(0, basket, price_list, offers)
    )

    return max(discounts)


def calculate_possible_discounts(accumulated_discount,
                                 basket,
                                 price_list,
                                 offers):
    discounts = [0]
    unchecked = [{"basket": basket, "accumulated_discount": 0}]

    while unchecked:
        current = unchecked.pop()
        for offer in offers:
            possibilities = offer(current["basket"], price_list)
            for possibility in possibilities:
                discounts.append(
                    current["accumulated_discount"] + possibility['discount']
                )
                unchecked.append({
                    "basket": possibility["basket"],
                    "accumulated_discount": possibility["discount"] + current["accumulated_discount"],
                })

    return discounts

def generate_combinations(items, quantity):
    if not items:
        raise Exception("generate_combinations called with empty items")

    if len(items) == 1:
        yield [items[0]] * quantity
    else:
        for i in range(0, quantity + 1):
            subitems = items[1:]
            for subset in generate_combinations(subitems, quantity - i):
                result = [items[0]] * i
                result.extend(subset)
                yield result

def calculate_x_for_y(x, y, basket, price_list):
    applies_to = ['ItemA', 'ItemB']

    combinations = generate_combinations(applies_to, x)
    #[(ItemA=3, ItemB=0), (ItemA=2, ItemB=1), (ItemA=1, ItemB=2), (etc...]

    # Iterate over combinations, see whether it fits the basket,
    # return discount if so. Combination fits basket if each item in
    # combination has at least that quantity in the basket.

    results = []

    for combination in combinations:
        new_basket = Basket(items=basket.items.copy())
        try:
            new_basket.remove_items(combination)
        except NotInBasketException:
            pass
        else:
            discount_items = itertools.combinations(combination, x - y)
            discounts = set()
            for possible_discount_items in discount_items:
                discounts.add(
                    sum(price_list[item] for item in possible_discount_items)
                )
            for discount in discounts:
                results.append({
                    'basket': new_basket,
                    'discount': discount
                })

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

    def __repr__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return sorted(self.items.items()) == sorted(other.items.items())

    # def __hash__(self):
    #     return hash(tuple(sorted(self.items.items())))

    def add_item(self, name, quantity):
        self.items[name] = self.items.get(name, 0) + quantity

    def remove_items(self, items):
        for item in items:
            self.remove_item(item, 1)

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
