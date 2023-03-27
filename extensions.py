import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')

        r = requests.get(f"https://v6.exchangerate-api.com/v6/ae27e1daf7ae42d268ec3410/pair/{base_key}/{sym_key}")
        resp = json.loads(r.content)
        new_price = resp['conversion_rate'] * float(amount)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message
