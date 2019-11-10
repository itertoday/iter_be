from core.models import Product
#I dont like this. will think on better strategies to implement it.
class DefaultStrategy:

    name = "default"

    @staticmethod
    def price(products, limit=2):
        total = 0
        for product in products:
            product_type, quantity = product['product_type'], product['quantity']
            
            if product_type == Product.RELOAD_PRODUCT_TYPE:
                if quantity >= limit:
                    total += quantity * 2500
                elif quantity > 0:
                    total += 3000
            
            if product_type == Product.NEW_PRODUCT_TYPE:
                total += quantity * 5000
        return total
            

            


class DummyStrategy:

    name = "dummy"

    @staticmethod
    def price(quantity, **kwargs):
        return 2500

PRICING_STRATEGIES = [ DefaultStrategy, DummyStrategy ]

