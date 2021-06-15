class Book:
    def __init__(self, author, title, shops=None):
        self.author = author
        self.title = title

        self.shops = shops
        self.shop = None

    def get_prices(self):
        for shop_object in self.shops:
            shop_object.get_price()
            if self.shop is None or shop_object.price < self.shop.price:
                self.shop = shop_object
