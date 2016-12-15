def calculate_discounts(basket, offers_list, price_list):
    quantities = {}
    for item in basket:
        quantities[item[0]] = quantities.get(item[0],0) + item[1]

    discount = 0
    for item in quantities.keys():
        if item in offers_list:
            offers = offers_list[item]
            if type(offers) is not list:
                offers = [offers]
            discount_function = DISCOUNTS[offers[0]]
            discount += discount_function(quantities[item], price_list[item])

    return discount

def calculate_discount_bogof(quantity, price):
    return (quantity / 2) * price

def calculate_discount_three_for_two(quantity, price):
    return (quantity / 3) * price

def calculate_discount_five_for_three(quantity, price):
    return (quantity / 5) * (price * 2)

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
