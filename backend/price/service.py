
#I dont like this. will think on better strategies to implement it.
class DefaultStrategy:

    name = "default"

    @staticmethod
    def price(quantity, **kwargs):
        print("dfs - quantity", quantity)
        print("kwargs", kwargs)
        limit = kwargs.get('limit', 4)
        request_type = kwargs.get('request_type')

        if request_type == "reload product":
            if quantity >= limit:
                return quantity * 2500
            return quantity * 3000
        
        if request_type == "new product":
            return quantity * 5000


class DummyStrategy:

    name = "dummy"

    @staticmethod
    def price(quantity, **kwargs):
        return 2500

PRICING_STRATEGIES = [ DefaultStrategy, DummyStrategy ]

