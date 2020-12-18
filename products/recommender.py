import redis
from products.models import Product

from django.conf import settings


# connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


class Recommender(object):

    @staticmethod
    def get_product_key(prod_id):
        return f'product:{prod_id}:purchased_with'

    def products_bought(self, products):
        product_ids = [p.id for p in products]

        for product_id in product_ids:
            for with_id in product_ids:
                # get the other products bought with each product
                if product_id != with_id:
                    # increment the score for the product purchased together
                    r.zincrby(self.get_product_key(product_id), 1, with_id)

    def suggest_products_for(self, products, max_tries=6):
        product_ids = [p.id for p in products]
        if len(products) == 1:
            suggestions = r.zrange(self.get_product_key(product_ids[0]), 0 , -1, desc=True)[:max_tries]
        else:
            # generate a temporary key
            flat_ids = ''.join(str(prod_id) for prod_id in product_ids)
            tmp_key = f'tmp_{flat_ids}'
            # multiple products, combine scores of all products
            # store the resultant sorted set in temporary key
            keys = [self.get_product_key(prod_id) for prod_id in product_ids]
            r.zunionstore(tmp_key, keys)
            # remove ids for the products the recommendation is for
            r.zrem(tmp_key, *product_ids)
            # get the product ids by their score, descendant sort
            suggestions = r.zrange(tmp_key, 0, -1, desc=True)[:max_tries]
            # remove the temporary key
            r.delete(tmp_key)

        suggested_product_ids = [int(prod_id) for prod_id in suggestions]
        # get suggested products and sort by order of appearance
        suggested_products = list(Product.objects.filter(id__in=suggested_product_ids))
        suggested_products.sort(key=lambda x: suggested_product_ids.index(x.id))
        return suggested_products

    def clear_purchases(self):
        for id in Product.objects.value_list('id', flat=True):
            r.delete(self.get_product_key(prod_id=id))


