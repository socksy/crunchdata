import entities

def get_products():
    raw_products = entities.get_endpoint('products')
    #TODO change this so we can sanely deal with pagination
    products = []
    for product in raw_products[:10]:
        products.append(entities.Entity(product))
        print('c')
    return products

