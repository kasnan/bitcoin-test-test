import sys
import time
import math
import base64
import hmac, hashlib

import pycurl
	
PY3 = sys.version_info[0] > 2
if PY3:
	import urllib.parse
else:
	import urllib

#import pycurl
import certifi
import json

trade_factor_in_price = 20000

rgParams = {
    "order_currency" : "BTC",
    "payment_currency" : "KRW"
}



class XCoinAPI:
	api_url = "https://api.bithumb.com";
	api_key = ""
	api_secret = ""

	def __init__(self, api_key, api_secret):
		self.api_key = api_key
		self.api_secret = api_secret

	def http_body_callback(self, buf):
		self.contents = buf

	def microtime(self, get_as_float = False):
		if get_as_float:
			return time.time()
		else:
			return '%f %d' % math.modf(time.time())

	def microsectime(self) :
		mt = self.microtime(False)
		mt_array = mt.split(" ")[:2]
		return mt_array[1] + mt_array[0][2:5]

	def xcoinApiCall(self, endpoint, rgParams):
		endpoint_item_array = {
			"endpoint" : endpoint
		}

		uri_array = dict(endpoint_item_array, **rgParams); 
		if PY3:
			e_uri_data = urllib.parse.urlencode(uri_array)
		else:
			e_uri_data = urllib.urlencode(uri_array)

		nonce = self.microsectime()

		hmac_key = self.api_secret
		utf8_hmac_key = hmac_key.encode('utf-8')

		hmac_data = endpoint + chr(0) + e_uri_data + chr(0) + nonce
		utf8_hmac_data = hmac_data.encode('utf-8')

		hmh = hmac.new(bytes(utf8_hmac_key), utf8_hmac_data, hashlib.sha512)
		hmac_hash_hex_output = hmh.hexdigest()
		utf8_hmac_hash_hex_output = hmac_hash_hex_output.encode('utf-8')
		utf8_hmac_hash = base64.b64encode(utf8_hmac_hash_hex_output)

		api_sign = utf8_hmac_hash
		utf8_api_sign = api_sign.decode('utf-8')

		# Connects to Bithumb API server and returns JSON result value.
		curl_handle = pycurl.Curl()
		curl_handle.setopt(pycurl.POST, 1)
		#curl_handle.setopt(pycurl.VERBOSE, 1); # vervose mode :: 1 => True, 0 => False
		curl_handle.setopt(pycurl.POSTFIELDS, e_uri_data)

		curl_handle.setopt(pycurl.CAINFO, certifi.where())

		url = self.api_url + endpoint
		curl_handle.setopt(curl_handle.URL, url)
		curl_handle.setopt(curl_handle.HTTPHEADER, ['Api-Key: ' + self.api_key, 'Api-Sign: ' + utf8_api_sign, 'Api-Nonce: ' + nonce])
		curl_handle.setopt(curl_handle.WRITEFUNCTION, self.http_body_callback)
		curl_handle.perform()

		#response_code = curl_handle.getinfo(pycurl.RESPONSE_CODE); # Get http response status code.

		curl_handle.close()

		return (json.loads(self.contents))


class Bithumb:
    def __init__(self) :
        self.access_key = "0ad40bbfacc75b17b79e8f22d2e35f66"
        self.secret_key = "15095dedb88a55d48065dbae12d9e139"
        self.btc_balance = 0
        self.krw_balance = 0
        self.api = XCoinAPI(self.access_key, self.secret_key)


    def get_current_price(self) :
        result = self.api.xcoinApiCall("/public/ticker", rgParams)
        #print("-----------------result: " + str(result))
        price = result["data"]["closing_price"]
        #print("[bithumb] get_current_price: " + str(price))
        
        return float(price)

    def buy_btc(self, price, amount) :
        rgParams = {
	        "order_currency" : "BTC",
	        "payment_currency" : "KRW",
            "units" : amount,
            "price" : price,
            "type" : "bid"
        }   

        result = self.api.xcoinApiCall("/trade/place", rgParams)
        print("[bithumb] btc but result: " + str(result))
        return result


    def buy_btc_market_price(self, amount) :
        price = self.get_current_price() + trade_factor_in_price
        rgParams = {
	        "order_currency" : "BTC",
	        "payment_currency" : "KRW",
            "units" : amount,
            "price" : int(price),
            "type" : "bid"
        }   
        result = self.api.xcoinApiCall("/trade/place", rgParams)
        print("[bithumb] buy btc market price result: " + str(result))
        return result

    def sell_btc(self, price, amount) :
        rgParams = {
	        "order_currency" : "BTC",
	        "payment_currency" : "KRW",
            "units" : amount,
            "price" : price,
            "type" : "ask"
        }   

        result = self.api.xcoinApiCall("/trade/place", rgParams)
        print("[bithumb] sell btc result: " + result)
        return result
        
    def sell_btc_market_price(self, amount) :
        
        price = self.get_current_price() - trade_factor_in_price
        rgParams = {
	        "order_currency" : "BTC",
	        "payment_currency" : "KRW",
            "units" : amount,
            "price" : int(price),
            "type" : "ask"
        }   

        result = self.api.xcoinApiCall("/trade/place", rgParams)
        print("[bithumb] sell btc market price result: " + str(result))
        return result

    def get_krw_balance(self) :
        result = self.api.xcoinApiCall("/info/balance", rgParams)
    
        return float(result["data"]["available_krw"])
    
    def get_btc_balance(self) :
        result = self.api.xcoinApiCall("/info/balance", rgParams)
    
        return float(result["data"]["available_btc"])


if __name__ =="__main__" :
    _bithumb = Bithumb()
    print(_bithumb.get_current_price())
    print(_bithumb.get_krw_balance())
    print(_bithumb.get_btc_balance())
    
    #_bithumb.sell(0.0001)
    #_bithumb.buy(0.0001)
    _bithumb.buy_btc_market_price(0.0001)
    _bithumb.sell_btc_market_price(0.0001)
    #print("current price: " + str(_bithumb.get_current_price()))
    time.sleep(100)
    