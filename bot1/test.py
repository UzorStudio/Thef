import telebot
import random
import base

import time
from secrets import token_bytes
from threading import Thread

import requests
from bs4 import BeautifulSoup
from coincurve import PublicKey
from _pysha3 import keccak_256


def genKey():
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]

    return {"private_key": private_key.hex(), "addr":f"0x{addr.hex()}"}

# 1. Собрать как можно больше адресов через скан
# 2. Генерировать приват кей и адрес и спрашивать у бд есть ли такой адрес
# 3. После успешной проверки отправлять сообщение? и добавлять в базу приват кей. ставить флажок TRUE на fuller
# не важно как долго, гланое чтоб работало постоянно
# не нужен доступ к интернету

# 1. Генерировать адрес и спрашивать по реквесту
# 2. Сохранять в бд если баланс больше 0
# Как ускорить процесс? Есть ли ограничения? не важно как долго, гланое чтоб работало постоянно
# Нужен доступ к интернету запускать на удаленной машине. Все отладить чтобы не нужно было проверять