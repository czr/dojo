class Basket(object):


    @classmethod
    def calculate_price(cls, basket, price_list, offers_list = {}):
        price = 0
        for item in basket:
            item_identifier = item[0]
            quantity = item[1]
            price += price_list[item_identifier] * quantity
        return price
