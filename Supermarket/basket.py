class Basket(object):

    @classmethod
    def calculate_price(cls, basket, price_list):
        return sum([price_list[item] for item in basket])
