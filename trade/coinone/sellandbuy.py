from json.decoder import JSONDecodeError
import urllib.request
from urllib.parse import urlencode
from urllib.request import ProxyBasicAuthHandler, Request, urlopen
import time
import base64
import hashlib
import hmac
import json
import time
import httplib2

bit_coin_amount = 0.0003

class Coinone:

    def __init__(self) :
        self.ACCESS_TOKEN = '5f26342e-9c93-4655-8018-81c3767258ee'
        self.SECRET_KEY = bytes('50b01c92-94f7-412e-882e-0cae2a64133b', 'utf-8')
        self.bit_coin_price = 0
        #self.update_bit_coin_price()

    def get_current_price(self) :       
        return float(self.get_bit_coin_price())

    def get_bit_coin_price(self) :
            
        urlTicker = urllib.request.urlopen('https://api.coinone.co.kr/ticker/?currency=BTC')
        readTicker = urlTicker.read()
        jsonTicker = json.loads(readTicker)
        #print("jsontiver, " + str(jsonTicker))
        #return jsonTicker["last"]
        return jsonTicker.get("last", -100000)
    
    def get_encoded_payload(self, payload):
        payload['nonce'] = int(time.time() * 1000)

        dumped_json = json.dumps(payload)
        encoded_json = base64.b64encode(bytes(dumped_json, 'utf-8'))
        return encoded_json


    def get_signature(self, encoded_payload):
        signature = hmac.new(self.SECRET_KEY, encoded_payload, hashlib.sha512)
        return signature.hexdigest()


    def get_response(self, action, payload):
        url = '{}{}'.format('https://api.coinone.co.kr/', action)

        encoded_payload = self.get_encoded_payload(payload)

        headers = {
            'Content-type': 'application/json',
            'X-COINONE-PAYLOAD': encoded_payload,
            'X-COINONE-SIGNATURE': self.get_signature(encoded_payload),
        }

        http = httplib2.Http()
        response, content = http.request(url, 'POST', body=encoded_payload, headers=headers)
        if response.status == 200 :
            return content
        else :
            print('[coinone] POST ERROR : ' + str(response.status))
            print('[coinone] ERROR ACTION : ' + str(action))
            print('[coinone] ERROR RESPONSE : ' + str(response) )
            print('[coinone] ERROR CONTENT : ' + str(content) )
            return content
        

    def buy_btc(self,price, amount) :
        #self.update_bit_coin_price()
    
       
        print('amount: ' + str(amount))
        result = self.get_response(action='v2/order/limit_buy', payload={
        'access_token': self.ACCESS_TOKEN,
        'price': price,
        'qty': amount,
        'currency': 'BTC',
        })
        print('[coinone] buy result : ')
        print('[coinone] btc buy amount: ' + str(amount))
        #print("[coinone] balance after buy" + str(self.get_krw_balance()))
        print(result)
    
    def sell_btc(self, price, amount) :
        #self.update_bit_coin_price()
        print('amount: ' + str(amount))
        result = self.get_response(action='v2/order/limit_sell', payload={
            'access_token': self.ACCESS_TOKEN,
            'price': price,
            'qty': amount,
            'currency': 'BTC',})
        print('[coinone] sell result : ')
        print('[coinone] btc sell amount: ' + str(amount))
        #print("[coinone] balance after sell" + str(self.get_krw_balance()))
        print(result)


    def get_user_balances(self) :
        result = self.get_response(action='v2/account/balance', payload={
        'access_token': self.ACCESS_TOKEN})
        result = json.loads(result)
        return result.get('krw'), result.get('btc')

    def get_krw_balance(self) :
        result = self.get_response(action='v2/account/balance', payload={
        'access_token': self.ACCESS_TOKEN})
        result = json.loads(result)
        return float(result.get('krw').get('avail'))

    def get_btc_balance(self) :
        result = self.get_response(action='v2/account/balance', payload={
        'access_token': self.ACCESS_TOKEN})
        result = json.loads(result)
        return float(result.get('btc').get('avail'))
        

if __name__ == "__main__" :
    _coinone = Coinone()
    #print(_coinone.get_current_price())
    
    #print(_coinone.get_btc_balance())
    
    #print(_coinone.get_krw_balance())

    #print('gloabal bit coin amount: '+ str(bit_coin_amount))
    _coinone.buy_btc(50100000, 0.0001)
   # _coinone.buy_btc(_coinone.get_current_price(), bit_coin_amount)
    time.sleep(100)
 