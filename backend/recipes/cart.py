from foodgram import settings


class Cart:

    def __init__(self, request):
        self.session = request.session
        self.cart = set(self.session.setdefault(settings.CART_SESSION_ID, []))

    def __iter__(self):
        for item in self.cart:
            yield item

    def __len__(self):
        return len(self.cart)

    def add(self, recipe):
        cart_len = len(self.cart)
        self.cart.add(recipe.id)
        self.save()
        return cart_len != len(self.cart)

    def save(self):
        self.session[settings.CART_SESSION_ID] = list(self.cart)
        self.session.modified = True

    def remove(self, recipe):
        cart_len = len(self.cart)
        self.cart.discard(recipe.id)
        self.save()
        return cart_len != len(self.cart)
