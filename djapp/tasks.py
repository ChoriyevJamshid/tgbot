import json
import logging
import time
import os
from celery import shared_task
from djapp.models import Product, Shop, ProductType, DataDict
from parsing.manage import run_parser

logger = logging.getLogger(__name__)


@shared_task
def task_1():
    logger.info('Task1 start')
    time.sleep(10)
    logger.info('Task1 end')


@shared_task
def get_parsing_data():
    logger.info("Parser is working!")
    run_parser()
    list_dirs = os.listdir('json_data')
    logger.info(f"Files: {list_dirs}")
    time.sleep(5)

    Product.objects.all().delete()

    for file_name in list_dirs:
        data = None
        dir_name = file_name.split('.')[0]

        try:
            logger.info(f"File name: {file_name}")
            with open(f'json_data/{file_name}', mode='r') as file:
                data = json.load(file)
                logger.info("\n\n")
                logger.info(data)
                logger.info("\n\n")

        except Exception as e:
            logger.info(f"\nError = {e}\n")

        if file_name == 'kwargs.json':
            DataDict.objects.all().delete()
            DataDict.objects.create(
                json_data=data,
                users_data=dict(),
                texts_data=dict(),
            )
            continue

        if data is None:
            print('\ndata is None\n')
            time.sleep(5)
            continue

        shop, created = Shop.objects.get_or_create(
            title=dir_name
        )
        logger.info(f'shop: {shop}')

        product_type, created = ProductType.objects.get_or_create(
            title='smartphone'
        )

        logger.info("\nSaving models\n")
        for page_number, page_data in data.items():
            # logger.info(f"Page number: {page_number}")
            for i, product in page_data.items():

                obj = Product(
                    title=product['title'],
                    link=product['link'],
                    price=product['price'],
                    shop=shop,
                    product_type=product_type
                )
                price_credit = product.get('price_credit')
                if price_credit:
                    obj.price_credit = price_credit

                obj.save()
                # logger.info(f"Product_{obj.pk} = {obj.title}")
                # logger.info(f'Created product: {obj}')





