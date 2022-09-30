import time

from main import redis, Product

key = 'order-completed'
group = 'products-groups'

try:
    redis.xgroup_create(name=key, groupname=group, mkstream=True)
    print('group created')
except Exception as e:
    print(e)

while True:
    try:
        results = redis.xreadgroup(consumername=key, groupname=group, streams={key: '>'})
        print(results)
        if results != []:
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity -= int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd(name='refund-order', fields=obj)
    except Exception as e:
        raise e
    time.sleep(3)
