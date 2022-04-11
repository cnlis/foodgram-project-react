from foodgram import settings


class Cart:

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault(settings.CART_SESSION_ID, [])

    def __len__(self):
        return len(self.cart)

    def __iter__(self):
        for item in self.cart:
            yield item

    def add(self, recipe):
        recipe_id = recipe.id
        if recipe_id not in self.cart:
            self.cart.append(recipe_id)
        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, recipe):
        recipe_id = recipe.id
        if recipe_id in self.cart:
            self.cart.remove(recipe_id)
            self.save()
