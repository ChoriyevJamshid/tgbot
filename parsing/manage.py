import asyncio
import json
import logging

from parsing import alifshop
from parsing import bemarket
from parsing import mediapark
from parsing import olcha
from parsing import sello
from parsing import texnomart
# from parsing import uzummarket
from parsing.base.parser import sync_recursion_dict_extend_dict

logger = logging.getLogger(__name__)


# async def async_run_tasks(tasks):
#     await asyncio.gather(*tasks)


def run_parser():
    logger.info("run_parer()() function is called")

    alifshop_parser = alifshop.parser.Parser(
        alifshop.parser.categories['smartphone']['category'],
        alifshop.parser.categories['smartphone']['subcategory'],
        *('alifshop', 'smartphone')
    )

    bemarket_parser = bemarket.parser.Parser(
        bemarket.parser.categories['smartphone']['category'],
        bemarket.parser.categories['smartphone']['subcategory'],
        *["bemarket", 'smartphone']
    )

    mediapark_parser = mediapark.parser.Parser(
        mediapark.parser.categories['smartphone']['category'],
        mediapark.parser.categories['smartphone']['subcategory'],
        *("mediapark", 'smartphone')
    )

    olcha_parser = olcha.parser.Parser(
        olcha.parser.categories['smartphone']['category'],
        olcha.parser.categories['smartphone']['subcategory'],
        *("olcha", 'smartphone')

    )

    sello_parser = sello.parser.Parser(
        sello.parser.categories['smartphone']['category'],
        sello.parser.categories['smartphone']['subcategory'],
        *("sello", 'smartphone')
    )

    texnomart_parser = texnomart.parser.Parser(
        texnomart.parser.categories['smartphone']['category'],
        texnomart.parser.categories['smartphone']['subcategory'],
        *("texnomart", 'smartphone')
    )

    # uzum_parser = uzummarket.parser.AsyncParser(
    #     uzummarket.parser.categories['smartphone']['category'],
    #     uzummarket.parser.categories['smartphone']['subcategory'],
    #     *("uzummarket", 'smartphone')
    # )

    # tasks = (
    #     alifshop_parser.run(),
    #     bemarket_parser.run(),
    #     mediapark_parser.run(),
    #     olcha_parser.run(),
    #     texnomart_parser.run(),
    #     sello_parser.run(),
    # )

    parser_list = (
        alifshop_parser,
        bemarket_parser,
        mediapark_parser,
        olcha_parser,
        texnomart_parser,
        sello_parser,
    )

    while True:
        try:
            asyncio.run(alifshop_parser.run())
            break
        except Exception as exc:
            print(alifshop_parser.__class__.__name__)
            print(exc)
            if alifshop_parser.exp_number > 3:
                break
            alifshop_parser.exp_number += 1
            print(exc)

    while True:
        try:
            asyncio.run(bemarket_parser.run())
            break
        except Exception as exc:
            print(bemarket_parser.__class__.__name__)
            print(exc)
            if bemarket_parser.exp_number > 3:
                break
            bemarket_parser.exp_number += 1
            print(exc)

    while True:
        try:
            asyncio.run(mediapark_parser.run())
            break
        except Exception as exc:
            print(mediapark_parser.__class__.__name__)
            print(exc)
            if mediapark_parser.exp_number > 3:
                break
            mediapark_parser.exp_number += 1
            print(exc)

    while True:
        try:
            asyncio.run(olcha_parser.run())
            break
        except Exception as exc:
            print(olcha_parser.__class__.__name__)
            print(exc)
            if olcha_parser.exp_number > 3:
                break
            olcha_parser.exp_number += 1
            print(exc)

    while True:
        try:
            asyncio.run(sello_parser.run())
            break
        except Exception as exc:
            print(sello_parser.__class__.__name__)
            print(exc)
            if sello_parser.exp_number > 3:
                break
            sello_parser.exp_number += 1
            print(exc)

    while True:
        try:
            asyncio.run(texnomart_parser.run())
            break
        except Exception as exc:
            print(texnomart_parser.__class__.__name__)
            print(exc)
            if texnomart_parser.exp_number > 3:
                break
            texnomart_parser.exp_number += 1
            print(exc)

    # while True:
    #     try:
    #         asyncio.run(uzum_parser.run())
    #         break
    #     except Exception as exc:
    #         print(uzum_parser.__class__.__name__)
    #         print(exc)
    #         if uzum_parser.exp_number > 3:
    #             break
    #         uzum_parser.exp_number += 1
    kwargs = dict()
    for parser in parser_list:
        sync_recursion_dict_extend_dict(kwargs, parser.kwargs)

    with open('json_data/kwargs.json', mode='w', encoding='utf-8') as file:
        json.dump(kwargs, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    run_parser()
