from langs import languages


def save_to_database(data_dict):
    data_dict.texts_data = {
        'uz': languages.uz,
        'ru': languages.ru,
        'en': languages.en
    }
    data_dict.save()

