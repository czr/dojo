def calculate_discount(quantities, offers_list, price_list):
    discount = 0
    for item in quantities.keys():
        if item in offers_list and offers_list[item] == 'bogof':
            discount += (quantities[item] / 2) * price_list[item]

    return discount

def calculate_price(basket, price_list, offers_list = {}):
    # offers_list = { 'ItemA': 'bogof' }
    quantities = {}
    for item in basket:
        quantities[item[0]] = quantities.get(item[0],0) + item[1]

    price = 0
    for item in quantities.keys():
        price += price_list[item] * quantities[item]

    discount = calculate_discount(quantities, offers_list, price_list)

    return price - discount
