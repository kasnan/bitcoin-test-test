from time import time
from trade.bithumb import bithumb
# from trade.coinone import sellandbuy
from trade.korbit import korbit_trade_test
#from trade.upbit import main
import pykorbit

_bithumb = bithumb.Bithumb()
# _coinone = sellandbuy.Coinone()
_korbit = korbit_trade_test.Korbit()
#_upbit = main.Upbit()



portfolio_btc= _korbit.get_btc_balance() +  +  _bithumb.get_btc_balance() #+ _coinone.get_btc_balance()
     
portfolio_cash = _korbit.get_krw_balance()+  _bithumb.get_krw_balance() #+ _coinone.get_krw_balance()        


portfolio = portfolio_btc * _korbit.get_current_price() + portfolio_cash
print("profolio : " + str(portfolio))
print("portfolio_btc: " + str(portfolio_btc))
print("portfolio_krw: " + str(portfolio_cash)+'\n')

averagePrice =_korbit.get_current_price() + _bithumb.get_current_price() #+ _coinone.get_current_price()
averagePrice = averagePrice/2

print('average  price: ' + str(averagePrice))


print('------------------check start time ------------------------')
print('portfolio: ' + str(portfolio) )
print('average  price: ' + str(averagePrice))
#save.insert_row(portFolio, averagePrice, 'any', round_number, trade_center_p)

print('------------------check end time --------------------------')


