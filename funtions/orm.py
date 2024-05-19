from django.db.models import Min, F

from djapp.models import Product


def get_product_from_db(values: list):
    products = Product.objects.all()
    for value in values:
        products = products.filter(
            title__icontains=value.lower()
        )

    min_price = products.aggregate(
        price=Min('price')
    )['price']

    product = products.filter(
        price=min_price
    ).first()

    return product
