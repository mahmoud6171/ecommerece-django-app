from decimal import Decimal
from django.urls import reverse
from store.models import Product

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

    def update(self, product, qty):
        product_id = str(product)
        product_quantity = qty

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_quantity

        self.session.modified = True

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()

        for product in products:
            product_dict = {
                'id': product.id,
                'title': product.title,
                'brand': product.brand,
                'price': str(product.price),
                'image': {'url': product.image.url if product.image else ''},
                'get_absolute_url': reverse('product_info', args=[product.slug])
            }
            cart[str(product.id)]['product'] = product_dict

        for item in cart.values():
            item['price'] = float(item['price'])
            item['total'] = str(item['price'] * item['qty'])
            yield item

    def get_total(self):
        return sum(float(item['price']) * item['qty'] for item in self.cart.values())




  


