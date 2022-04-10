from foodgram import settings


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        return len(self.cart.keys())

    def __iter__(self):
        for item in self.cart.keys():
            yield int(item)

    def add(self, recipe):
        recipe_id = str(recipe.id)
        if recipe_id not in self.cart:
            self.cart[recipe_id] = True
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, recipe):
        recipe_id = str(recipe.id)
        if recipe_id in self.cart:
            del self.cart[recipe_id]
            self.save()
