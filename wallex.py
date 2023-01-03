import time
import datetime
import csv

import undetected_chromedriver.v2 as uc
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import undetected_chromedriver.v2 as uc

import binance
from binance.client import Client
from binance.websockets import BinanceSocketManager
from binance.exceptions import BinanceAPIException, BinanceOrderException
from twisted.internet import reactor

api_key = 'your-api-key'
api_secret = 'your-api-secret'


class Wallex():
    def __init__(self):
        self.username = 'your-user'
        self.password = 'your-pass'
        # caps = DesiredCapabilities().CHROME
        # caps["pageLoadStrategy"] = "normal"  #  complete
        # caps["pageLoadStrategy"] = "eager"  #  interactive
        #caps["pageLoadStrategy"] = "none"
        # self.driver = webdriver.Chrome(desired_capabilities=caps, executable_path=ChromeDriverManager().install())
        # options = Options()
        # options.add_argument('--headless')
        # self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        # self.driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
        # capabilities = DesiredCapabilities.FIREFOX
        # capabilities["marionette"] = True
        # fp = webdriver.FirefoxProfile()
        # fp.set_preference("http.response.timeout", 20)
        # fp.set_preference("dom.max_script_run_time", 20)
        # self.driver = webdriver.Firefox(capabilities=capabilities, executable_path=GeckoDriverManager().install())

        # self.driver = webdriver.Firefox(executable_path=GeckoDriverManager('v0.27.0').install())

        # self.driver.command_executor()
        # self.driver = uc.Chrome()
        self.login_url = 'https://wallex.ir/app/auth/login'
        self.asset_url = 'https://wallex.ir/app/trade/eth-usdt'
        


        self.bch_bid_ask = {'buy_price': 0, 'buy_volume': 0, 'sell_price': 0, 'sell_volume': 0}

        self.orderbook_sell = []
        self.orderbook_buy = []

        self.coin_balance = 0
        self.tether_balance = 0

        self.cookies_file ='cookies.txt'
        self.cookies = []

    def login_undetected_chrome(self):
        driver = uc.Chrome()
        with driver:
            driver.get(self.login_url)

        driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
        driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        driver.find_element_by_xpath('//*[@id="signup-form_id"]/div[4]/div/input').click()
        code = input('verification code: ')
        driver.find_element_by_xpath('//*[@id="two_fa_code"]').send_keys(code)
        driver.find_element_by_xpath('//*[@id="signup-form_id"]/div[2]/div/input').click()

        time.sleep(5)
        self.cookies = driver.get_cookies()
        open(self.cookies_file, 'w').close()
        with open(self.cookies_file, mode='a') as f:
            for cookie in self.cookies:
                f.write(str(cookie) + '\n')
        print('saved cookies')
        driver.quit()
        time.sleep(1)


    def login(self):
        self.driver.get(self.login_url)
        time.sleep(10)
        # self.driver.implicitly_wait(5)
        self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.username)
        self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(self.password)
        self.driver.find_element_by_xpath('//*[@id="signup-form_id"]/div[4]/div/input').click()
        code = input('verification code: ')
        self.driver.find_element_by_xpath('//*[@id="two_fa_code"]').send_keys(code)
        self.driver.find_element_by_xpath('//*[@id="signup-form_id"]/div[2]/div/input').click()

        time.sleep(5)
        self.cookies = self.driver.get_cookies()
        open(self.cookies_file, 'w').close()
        with open(self.cookies_file, mode='a') as f:
            for cookie in self.cookies:
                f.write(str(cookie) + '\n')
        print('saved cookies')

    def set_cookies(self):
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get('https://wallex.ir')
        with open(self.cookies_file, mode='r') as f:
            for line in f.readlines():
                self.driver.add_cookie(eval(line.strip()))
        self.driver.get(self.asset_url)
        print('cookie set completed')

    def goto_bch(self):
        self.driver.get(self.asset_url)
        self.driver.find_element_by_xpath('//*[@id="app"]/header/nav/div[2]/span/form/label[2]').click()
        time.sleep(8)
        # self.driver.find_element_by_link_text('فروش سریع').click()
        # self.driver.find_element_by_link_text('خرید سریع').click()

    def update_bch_price(self):
        counter = 0
        limit = 5
        while counter < limit:
            try:
                self.bch_bid_ask['sell_price'] = self.driver.find_element_by_xpath('//*[@id="sellers-table"]/tbody').text.split(' ')[1].replace(',', '')
                self.bch_bid_ask['sell_price'] = float(self.bch_bid_ask['sell_price'])

                self.bch_bid_ask['sell_volume'] = self.driver.find_element_by_xpath('//*[@id="sellers-table"]/tbody').text.split(' ')[0].replace(',', '')
                self.bch_bid_ask['sell_volume'] = float(self.bch_bid_ask['sell_volume'])

                self.bch_bid_ask['buy_price'] = self.driver.find_element_by_xpath('//*[@id="buyers-table"]/tbody').text.split(' ')[1].replace(',', '')
                self.bch_bid_ask['buy_price'] = float(self.bch_bid_ask['buy_price'])

                self.bch_bid_ask['buy_volume'] = self.driver.find_element_by_xpath('//*[@id="buyers-table"]/tbody').text.split(' ')[0].replace(',', '')
                self.bch_bid_ask['buy_volume'] = float(self.bch_bid_ask['buy_volume'])
                break
            except:
                time.sleep(1)
                counter += 1
            if counter == limit - 2:
                self.driver.refresh()
                time.sleep(6)
                counter += 1
            if counter == limit - 1:
                print('error loading buy/sell tables')
                print('reloading...')
                counter = 0

    def get_coin_balance(self):
        self.coin_balance = float(self.driver.find_element_by_xpath('//*[@id="av-co-v-inner"]').text)
        return self.coin_balance

    def get_tether_balance(self):
        self.tether_balance = float(self.driver.find_element_by_xpath('//*[@id="av-mo-v-inner"]').text)
        return self.tether_balance

    def sell_bch(self, volume):
        counter = 0
        limit = 3
        while counter < limit:
            try:
                self.clear_sell_fields()
                self.driver.find_element_by_xpath('//*[@id="sell_value"]').send_keys(str(volume))
                self.driver.find_element_by_xpath('//*[@id="ma-pr-su"]').click()
                self.driver.find_element_by_xpath('//*[@id="sellorder"]/div[3]/div/button').click()
                time.sleep(5)
                return True
            except:
                time.sleep(1)
                counter += 1
        print('couldn\'t sell :(')
        return False

    def buy_bch(self, volume):
        counter = 0
        limit = 3
        while counter < limit:
            try:
                self.clear_buy_fields()
                self.driver.find_element_by_xpath('//*[@id="buy_value"]').send_keys(str(volume))
                self.driver.find_element_by_xpath('//*[@id="lo-pr-su"]').click()
                self.driver.find_element_by_xpath('//*[@id="buyorder"]/div[3]/div/button').click()
                time.sleep(5)
                return True
            except:
                time.sleep(1)
                counter += 1
        print('couldn\'t sell :(')
        return False

    def cancel_incomplete_order(self):
        if wallex.driver.find_element_by_xpath('//*[@id="pjax-container"]/section[2]/div/div/div[7]/div/div[2]/div/table/tbody/tr/td[6]/a/button').text:
            while True:
                try:
                    wallex.driver.find_element_by_xpath('//*[@id="pjax-container"]/section[2]/div/div/div[7]/div/div[2]/div/table/tbody/tr/td[6]/a/button').click()
                    time.sleep(0.5)
                    wallex.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[1]').click()
                    time.sleep(0.5)
                    wallex.driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/button[1]').click()
                    time.sleep(0.5)
                    break
                except:
                    print('error in canceling incomplete order')
        else:
            # todo: check kardane balance, age kam shode bood doroste vagarna refresh kone ta cancel kone
            pass


    def clear_sell_fields(self):
        self.driver.find_element_by_xpath('//*[@id="sell_value"]').clear()
        self.driver.find_element_by_xpath('//*[@id="sell_price"]').clear()

    def clear_buy_fields(self):
        self.driver.find_element_by_xpath('//*[@id="buy_value"]').clear()
        self.driver.find_element_by_xpath('//*[@id="buy_price"]').clear()

    def get_orderbook_sell(self):
        while True:
            try:
                sell_raw_1 = self.driver.find_element_by_xpath('//*[@id="sellers-table"]/tbody').text.split('\n')
                break
            except:
                self.driver.refresh()
                time.sleep(6)
                print('refreshed. orderbook error')
        sell_raw_2 = []
        for els in sell_raw_1:
            for el in els.split(' '):
                sell_raw_2.append(float(el.replace(',', '')))
        self.orderbook_sell = sell_raw_2
        # print(sell_raw_2)

    def get_orderbook_buy(self):
        while True:
            try:
                buy_raw_1 = self.driver.find_element_by_xpath('//*[@id="buyers-table"]/tbody').text.split('\n')
                break
            except:
                self.driver.refresh()
                time.sleep(6)
                print('refreshed. orderbook error')
        buy_raw_2 = []
        for els in buy_raw_1:
            for el in els.split(' '):
                buy_raw_2.append(float(el.replace(',', '')))
        self.orderbook_buy = buy_raw_2
        # print(sell_raw_2)

    def save_data_in_file(self, data, filename):
        with open(filename, mode='a') as file:
            data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            data_writer.writerow([datetime.datetime.now()] + data)
            # file.write([datetime.datetime.now()] + data)

    def is_orderbook_sell_changed(self):
        orderbook_sell_raw = self.orderbook_sell
        self.get_orderbook_sell()
        return not(orderbook_sell_raw == self.orderbook_sell)

    def is_orderbook_buy_changed(self):
        orderbook_buy_raw = self.orderbook_buy
        self.get_orderbook_buy()
        return not(orderbook_buy_raw == self.orderbook_buy)

# wallex = Wallex()
# wallex.driver.get('https://wallex.ir/markets/eth-usdt')
# with open('wallex_eth_orderbook.csv', mode='a') as file:
#     data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     while True:
#         # time.sleep(1)
#         try:
#             if wallex.is_orderbook_buy_changed():
#                 data_writer.writerow(['buy', datetime.datetime.now()] + wallex.orderbook_buy)
#                 file.flush()
#                 print('buy')
#             if wallex.is_orderbook_sell_changed():
#                 data_writer.writerow(['sell', datetime.datetime.now()] + wallex.orderbook_sell)
#                 file.flush()
#                 print('sell')
#         except:
#             wallex.driver.get('https://wallex.ir/markets/eth-usdt')

########################################################

# def btc_trade_history(msg):
#     if msg['e'] != 'error':
#         price['BCHUSDT'] = float(msg['b'])
#         binance_file_data_writer.writerow([datetime.datetime.now(), float(msg['b'])])
#         binance_file.flush()
#     else:
#         price['error']: True
#
# price = {'BCHUSDT': None, 'error': False}

# binance_file = open('binance_eth_price.csv', mode='a')
# binance_file_data_writer = csv.writer(binance_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
# client = Client(api_key, api_secret)
# # print(client.futures_account_balance())
# bsm = BinanceSocketManager(client)
# # conn_key = bsm.start_symbol_ticker_socket('BCHUSDT', btc_trade_history)
# conn_key = bsm.start_symbol_ticker_socket('ETHUSDT', btc_trade_history)
# bsm.start()


wallex = Wallex()
# wallex.login()
# wallex.login_undetected_chrome()
wallex.set_cookies()
wallex.goto_bch()
wallex.update_bch_price()


CW = 0.002
CB = 0.001
diff = 70
test_volume = 0.005
counter = 0

while True:
    time.sleep(2)
    # if wallex.is_orderbook_sell_changed():
    #     print('best sell update: ' + str(wallex.bch_bid_ask['sell_price']))
    # if wallex.is_orderbook_buy_changed():
    #     print('best buy update: ' + str(wallex.bch_bid_ask['buy_price']))
    while True:
        now = datetime.datetime.now()
        try:
            wallex.update_bch_price()
            wallex.get_tether_balance()
            wallex.get_coin_balance()
            break
        except:
            if (datetime.datetime.now()-now).seconds > 4:
                print('cant find balances in wallex')


    print('wallex sell: ' + str(wallex.bch_bid_ask['sell_price']))
    print('wallex buy: ' + str(wallex.bch_bid_ask['buy_price']))
    print('binance price: ' + str(price['BCHUSDT']) + '\n')
    print('sell at wallex: ' + str(wallex.bch_bid_ask['buy_price']*(1-CW) - price['BCHUSDT']*(1+CB)))
    print('buy at wallex: ' + str(price['BCHUSDT']*(1-CB) - wallex.bch_bid_ask['sell_price']*(1+CW)))

    if wallex.bch_bid_ask['buy_price']*(1-CW) - price['BCHUSDT']*(1+CB) > diff:
        input('sell?')
        proper_volume = min(test_volume, wallex.bch_bid_ask['buy_volume'])
        # proper_volume = test_volume
        # order = client.order_market(symbol='BCHUSDT', side=Client.SIDE_BUY, quantity=proper_volume)
        if float(client.get_asset_balance('USDT')['free']) >= proper_volume * price['BCHUSDT']*(1+CB) and wallex.coin_balance > proper_volume*(1+CW):
            initial_balance = wallex.coin_balance
            if wallex.sell_bch(proper_volume):
                order = client.order_market(symbol='ETHUSDT', side=Client.SIDE_BUY, quantity=proper_volume)
                # if wallex.get_coin_balance()*(1-CW) - initial_balance < proper_volume * 0.999:
                #     wallex.cancel_incomplete_order()
                #     # todo: meghdare canceli ro bigiram va estefade az code cancel order tooye binance
                counter += 1
                print('sell coin at wallex :)')
                time.sleep(5)
            else:
                print('error in sell at wallex')
                wallex.driver.refresh()
                time.sleep(6)
        else:
            print('balance is insufficient')

    if price['BCHUSDT']*(1-CB) - wallex.bch_bid_ask['sell_price']*(1+CW) > diff:
        input('buy?')
        proper_volume = min(test_volume, wallex.bch_bid_ask['sell_volume'])
        # proper_volume = test_volume
        # order = client.order_market(symbol='BCHUSDT', side=Client.SIDE_SELL, quantity=proper_volume)
        if float(client.get_asset_balance('ETH')['free']) >= proper_volume and wallex.tether_balance > proper_volume * wallex.bch_bid_ask['sell_price'] * (1+CW):
            if wallex.buy_bch(proper_volume):
                order = client.order_market(symbol='ETHUSDT', side=Client.SIDE_SELL, quantity=proper_volume)
                counter += 1
                print('buy coin at wallex :)')
                time.sleep(5)
            else:
                print('error in buy at wallex')
                wallex.driver.refresh()
                time.sleep(6)
        else:
            print('balance is insufficient')

    print('################')




# with open('wallex_eth_orderbook.csv', mode='a') as file:
#     data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#     while True:
#         # time.sleep(1)
#         if wallex.is_orderbook_buy_changed():
#             data_writer.writerow(['buy', datetime.datetime.now()] + wallex.orderbook_buy)
#             file.flush()
#             print('buy')
#         if wallex.is_orderbook_sell_changed():
#             data_writer.writerow(['sell', datetime.datetime.now()] + wallex.orderbook_sell)
#             file.flush()
#             print('sell')
