from django.db.models import Min, F, Q, Prefetch

from djapp.models import Product, Shop, DataDict, User, UserHistory


def get_product_from_db(values: list) -> list:
    """
    parameters: values[list]
    return -> list
    """
    # Create Q objects using values:list
    query = Q()
    for value in values:
        lookup = "{}__icontains".format('title')
        query &= Q(**{lookup: value})

    # get all shops and filtering products using <query>
    shops = Shop.objects.all().prefetch_related(
        Prefetch(
            "products",
            queryset=Product.objects.filter(query)
        )
    )

    products = []
    for shop in shops:
        # get minimum price from shop filtering product
        min_price = shop.products.all().aggregate(
            price=Min('price')
        )['price']

        # get product which price is minimum and append into list
        product = shop.products.filter(price=min_price).first()
        if product:
            price = float(product.price)
            # print(f"shop: {shop.title}, len: {len(shop.products.all())}, min_price: {min_price}")
            products.append(
                {
                    'shop': shop.title,
                    'product': product,
                    'price': price
                }
            )
    return products


data_dict = DataDict.objects.all().first()


def save_users_data(users_data, chat_id, user_data):
    users_data[str(chat_id)] = user_data
    data_dict.users_data = users_data
    data_dict.save()


def get_or_create_user(session, chat_id, first_name='', username=''):
    created = False
    if session.get(str(chat_id), None) is None:
        user, created = User.objects.get_or_create(chat_id=chat_id)
        if created:
            user.first_name = first_name
            user.username = username
            user.save()
        session[str(chat_id)] = {"user": user}
    user = session[str(chat_id)]['user']

    return user, created


def save_user_history(user, text, values):
    history, created = UserHistory.objects.get_or_create(user=user)

    if created:
        history.texts['texts'] = list()
        history.values['values'] = list()

    history.texts['texts'].append(text)
    history.values['values'].append(values)
    history.save()


def get_users_number():
    return User.objects.count()


def get_users():
    return User.objects.all()


def get_user_history(user):
    return UserHistory.objects.filter(
        user=user
    ).first()

