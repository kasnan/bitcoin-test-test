import json
import requests 
import time

class Korbit :
    def __init__(self) -> None:
        self.client_id = 'uihAxApaUfXxD1fyHEjC1UTWHZOwFQ1VPY8cKyUkeqWpAdSnJ1WQVp2yUgoqD'
        self.client_secret = 'O210R4Tuqgpv7eAByhMMFL2hlxrH5jSrCv7hbU7Vrm985lGkGPer9Q5x5QuZk'
        self.headers = ""

        self.update_header()
        print('current access token is ' + str(self.client_id))
        
    def get_access_token(self) :
        access_data = {'client_id' : self.client_id, 'client_secret' : self.client_secret,'grant_type' : 'client_credentials'}
        response = requests.post('https://api.korbit.co.kr/v1/oauth2/access_token', data=access_data)
        access_json = response.json()
        access_token = access_json.get('access_token')
        return access_token

    def update_header(self) :
        access_token = self.get_access_token()
        self.headers = {
            'Authorization': f"Bearer {access_token}",
        }

    def get_current_price(self) :
        currency = "btc_krw"
        url = "https://api.korbit.co.kr/v1/ticker"
        
        response = requests.get(url)

        return float(response.json().get('last'))

    def get_user_balances(self) :
        self.update_header()
        response = requests.get('https://api.korbit.co.kr/v1/user/balances', headers=self.headers)
        print(response)
        print("krw balance : " + str(response.json().get('krw')))
        print("btc balance : " + str(response.json().get('btc')))

    # 빈도가 낮게 에러 발생
    def get_krw_balance(self) :
        self.update_header()
        response = requests.get('https://api.korbit.co.kr/v1/user/balances', headers=self.headers)
        if response.status_code == 200 :
            balance = float(response.json().get('krw').get('available'))
            return balance
        else :
            print('[korbit] fail to get krw balance')
            print(response)
            return -1000000000
            

    def get_btc_balance(self) :
        self.update_header()
        response = requests.get('https://api.korbit.co.kr/v1/user/balances', headers=self.headers)
        if response.status_code == 200 :
            balance = float(response.json().get('btc').get('available'))
            return balance
        else :
            print('[korbit] fail to get btc balance')
            print(response)
            return -1000000000

    def buy_btc_market_price(self, amount) :
        self.update_header()
        buy_data = {
            'currency_pair' : 'btc_krw',
            'type' :'market',
            'price' : self.get_current_price(),
            'coin_amount' : amount,
        }
        response = requests.post('https://api.korbit.co.kr/v1/user/orders/buy',headers=self.headers, data=buy_data)
        print('[korbit] buy result : ')
        if response.status_code == 200 :
            print("[korbit] success to buy btc market_price")
            print(response.json())
            print("[korbit] krw balance after sell" + str(self.get_krw_balance()))
        else :
            print('[korbit] fail to buy btc market_price')
            print(response.status_code)
            print(response.json())

    def sell_btc_market_price(self, amount) :
        self.update_header()
        #korbit = pykorbit.Korbit('ygra123@gmail.com', 'OllehYgra$1', self.client_id, self.client_secret)
        #order = korbit.sell_limit_order("BTC", str(self.get_current_price()), amount)
        sell_data = {
            'currency_pair' : 'btc_krw',
            'type' :'market',
            'price': self.get_current_price(),
            'coin_amount' : amount,
        }
        response = requests.post('https://api.korbit.co.kr/v1/user/orders/sell',headers=self.headers, data=sell_data)
        print('[korbit] sell result : ')
        if response.status_code == 200 :
            print("[korbit] success to sell btcmarket_price")
            print(response.json())
            print(response)
            print("[korbit] krw balance after sell" + str(self.get_krw_balance()))
        else :
            print('[korbit] fail to sell btc market_price')
            print(response.status_code)
            print(response.json())



    def buy_btc(self, price, amount) :
        print("[korbit] buy btc : "+ "price: "+ str(price) + "amount "+ str(amount))
        self.update_header()
        buy_data = {
            'currency_pair' : 'btc_krw',
            'type' :'limit',
            'price' : price,
            'coin_amount' : amount,
        }
        response = requests.post('https://api.korbit.co.kr/v1/user/orders/buy',headers=self.headers, data=buy_data)
        print('[korbit] buy result : ')
        if response.status_code == 200 :
            print("[korbit] success to buy btc")
            print(response.json())
            print("[korbit] krw balance after buy" + str(self.get_krw_balance()))
        else :
            print('[korbit] fail to buy btc')
            print(response.status_code)
            print(response.json())

    def sell_btc(self, price, amount) :
        print("[korbit] sell btc : "+ "price: " + str(price) + "amount: " + str(amount))
        self.update_header()
        sell_data = {
            'currency_pair' : 'btc_krw',
            'type' :'limit',
            'price': price,
            'coin_amount' : amount,
        }
        response = requests.post('https://api.korbit.co.kr/v1/user/orders/sell',headers=self.headers, data=sell_data)
        print('[korbit] sell result : ')
        if response.status_code == 200 :
            print("success to sell btc")
            print(response.json())
            print(response)
            print("[korbit] krw balance after sell" + str(self.get_krw_balance()))
        else :
            print('[korbit] fail to sell btc')
            print(response.status_code)
            print(response.json())

if __name__ =="__main__" :
    _korbit = Korbit()
    print(_korbit.get_current_price())
    #print("get krw before: " + str(_korbit.get_krw_balance()))
    #print("get btc before" + str(_korbit.get_btc_balance()))
    #print(_korbit.buy_btc(_korbit.get_current_price()+100000, 0.0001))
    #print(_korbit.sell_btc(_korbit.get_current_price() - 100000, 0.0001))
    print("get btc: " + str(_korbit.get_btc_balance()))
    print("get krw: " + str(_korbit.get_krw_balance()))

    time.sleep(100)