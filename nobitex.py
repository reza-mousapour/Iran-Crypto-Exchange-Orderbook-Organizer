from datetime import datetime, timedelta
import time
import pymongo
import csv

import binance
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.firefox import GeckoDriverManager

class Nobitex():
    def __init__(self):
        self.login_url = 'https://nobitex.ir/login/'
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.get(self.login_url)

        self.btc_url = 'https://nobitex.ir/app/exchange/trx-usdt/'
        self.commission_binance = 0.001
        self.commission_nobitex = 0.0015


    def login(self, username, password):
        self.driver.find_element_by_xpath('//*[@id="email-div"]/input').send_keys(nobitex_login_data['user'])
        self.driver.find_element_by_xpath('//*[@id="iPassword"]').send_keys(nobitex_login_data['pass'])
        input()
        self.driver.find_element_by_xpath('//*[@id="submit"]').click()
        time.sleep(3)

    def arbitrage_btc(self):
        self.driver.get(self.btc_url)
        time.sleep(3)

        buy_orderbook_raw = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[2]/div').text.split()[9:]
        sell_orderbook_raw = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[1]/div').text.split()[9:]

        buy_orderbook = buy_orderbook_raw
        sell_orderbook = sell_orderbook_raw

        if





nobitex_login_url = 'https://nobitex.ir/login/'
nobitex_login_data = {'user': 'your-user', 'pass': 'your-pass'}
login_driver = webdriver.Chrome(ChromeDriverManager().install())
login_driver.get(nobitex_login_url)

print(nobitex_login_data['user'])
time.sleep(1)
login_driver.find_element_by_xpath('//*[@id="email-div"]/input').send_keys(nobitex_login_data['user'])
login_driver.find_element_by_xpath('//*[@id="iPassword"]').send_keys(nobitex_login_data['pass'])
input()
login_driver.find_element_by_xpath('//*[@id="submit"]').click()
time.sleep(5)

# login_driver.get('https://nobitex.ir/app/exchange/btc-usdt/')
login_driver.get('https://nobitex.ir/app/exchange/trx-usdt/')

buy_orderbook_raw = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[2]/div').text.split()[9:]
sell_orderbook_raw = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[1]/div').text.split()[9:]

buy_orderbook = buy_orderbook_raw
sell_orderbook = sell_orderbook_raw

print('start')
commission_binance = 0.001
commission_nobitex = 0.0015

total = 0

# buy
# login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/div/p[2]/a').click()
# login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/form/div[1]/div/input').send_keys()
# login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/div/span/button').click()
def buy_from_nobitex(volume):
    login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/div/p[2]/a').click()
    login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/form/div[1]/div/input').send_keys(str(volume))
    login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div/div[3]/div/span/button').click()


while True:
    buy_orderbook = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[2]/div').text.split()[9:]
    sell_orderbook = login_driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[3]/div[1]/div').text.split()[9:]

    if sell_orderbook_raw != sell_orderbook:
        print('update sell!')
        buy_price = float(buy_orderbook[1].replace(',', ''))
        buy_volume = float(buy_orderbook[2].replace(',', ''))
        sell_price = float(sell_orderbook[1].replace(',', ''))
        sell_volume = float(sell_orderbook[2].replace(',', ''))
        if data['BTCUSDT_price']*(1+commission_binance) < sell_price*(1-commission_nobitex):
            total += (sell_price*sell_volume*(1-commission_nobitex) - data['BTCUSDT_price']*sell_volume(1+commission_binance))
            print('total: ' + str(total))
        print(str(data['BTCUSDT_price']) + ', ' + str(sell_price))
        sell_orderbook_raw = sell_orderbook

    if buy_orderbook_raw != buy_orderbook:
        print('update buy!')
        buy_price = float(buy_orderbook[1].replace(',', ''))
        buy_volume = float(buy_orderbook[2].replace(',', ''))
        sell_price = float(sell_orderbook[1].replace(',', ''))
        sell_volume = float(sell_orderbook[2].replace(',', ''))
        if buy_price*(1+commission_nobitex) < data['BTCUSDT_price']*(1-commission_binance):
            total += (data['BTCUSDT_price']*buy_volume*(1-commission_binance) - buy_price*buy_volume*(1+commission_nobitex))
            print('total: ' + str(total))
        print(str(data['BTCUSDT_price']) + ', ' + str(buy_price))
        buy_orderbook_raw = buy_orderbook




# bsm.stop_socket(conn_key)
# reactor.stop()


############################################################
############################################################

api_key = 'your-api-key'
api_secret = 'your-api-secret'

client = Client(api_key, api_secret)
data={'BTCUSDT_price':0}
def process_symbol_ticker_socket(msg):
    if msg['e'] != 'error':
        # print(str(datetime.now()) + ': ' + msg['b'])
        data['BTCUSDT_price'] = float(msg['b'])

bsm = BinanceSocketManager(client)
conn_key = bsm.start_symbol_ticker_socket('BTCUSDT', process_symbol_ticker_socket)
bsm.start()

client = pymongo.MongoClient('your-address', username='your-user', password='your-pass')

db = client.quantvan

nobitex_url = 'https://nobitex.ir/app/exchange/btc-usdt/'

driver = webdriver.Chrome(ChromeDriverManager().install())
# driver = webdriver.Chrome('/home/tensurf/Desktop/Data_record/chromedriver')
# driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
driver.get(nobitex_url)

buy_orderbook_raw = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div').text.split()[9:]
sell_orderbook_raw = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div').text.split()[9:]

buy_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div').text.split()[9:]
sell_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div').text.split()[9:]

print('start')
commission_binance = 0.001
commission_nobitex = 0.0015

total = 0


while True:
    buy_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div').text.split()[9:]
    sell_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div').text.split()[9:]

    if sell_orderbook_raw != sell_orderbook:
        print('update sell!')
        buy_price = float(buy_orderbook[1].replace(',', ''))
        buy_volume = float(buy_orderbook[2].replace(',', ''))
        sell_price = float(sell_orderbook[1].replace(',', ''))
        sell_volume = float(sell_orderbook[2].replace(',', ''))
        if data['BTCUSDT_price']*(1+commission_binance) < sell_price*(1-commission_nobitex):
            total += (sell_price*sell_volume*(1-commission_nobitex) - data['BTCUSDT_price']*sell_volume(1+commission_binance))
            print('total: ' + str(total))
        print(str(data['BTCUSDT_price']) + ', ' + str(sell_price))
        sell_orderbook_raw = sell_orderbook

    if buy_orderbook_raw != buy_orderbook:
        print('update buy!')
        buy_price = float(buy_orderbook[1].replace(',', ''))
        buy_volume = float(buy_orderbook[2].replace(',', ''))
        sell_price = float(sell_orderbook[1].replace(',', ''))
        sell_volume = float(sell_orderbook[2].replace(',', ''))
        if buy_price*(1+commission_nobitex) < data['BTCUSDT_price']*(1-commission_binance):
            total += (data['BTCUSDT_price']*buy_volume*(1-commission_binance) - buy_price*buy_volume*(1+commission_nobitex))
            print('total: ' + str(total))
        print(str(data['BTCUSDT_price']) + ', ' + str(buy_price))
        buy_orderbook_raw = buy_orderbook




# bsm.stop_socket(conn_key)
# reactor.stop()












with open('ask_bid_nobitex.csv', mode='w+') as ask_bid_file:
    ask_bid_writer = csv.writer(ask_bid_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    while True:
        buy_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[2]/div').text.split()[9:]
        sell_orderbook = driver.find_element_by_xpath('/html/body/div[1]/div/main/div/div/div/div[2]/div[1]/div').text.split()[9:]
        # print(buy_orderbook)
        # break
        if buy_orderbook_raw != buy_orderbook:
            # db.orderbook_bid_nbx.insert_one({
            #     'time': datetime.now(),
            #     'data': buy_orderbook_raw})
            ask_bid_writer.writerow(['bid', datetime.now()] + buy_orderbook)
            # print(str(counter) + ': ' + 'new bid: ' + str(datetime.now()))
            buy_orderbook_raw = buy_orderbook
            counter += 1
            print(counter)

        if sell_orderbook_raw != sell_orderbook:
            # db.orderbook_ask_nbx.insert_one({
            #     'time': datetime.now(),
            #     'data': sell_orderbook_raw})
            ask_bid_writer.writerow(['ask', datetime.now()] + buy_orderbook)
            # print(str(counter) + ': ' + 'new ask: ' + str(datetime.now()))
            sell_orderbook_raw = sell_orderbook
            counter += 1
            print(counter)

