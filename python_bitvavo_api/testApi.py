from python_bitvavo_api.bitvavo import Bitvavo
import sys
import signal
import time
import json

""" 
* This is an example utilising all functions of the python Bitvavo API wrapper.
* The APIKEY and APISECRET should be replaced by your own key and secret.
* For public functions the APIKEY and SECRET can be removed.
* Documentation: https://docs.bitvavo.com
* Bitvavo: https://bitvavo.com
* README: https://github.com/bitvavo/php-bitvavo-api
"""

def main():
  bitvavo = Bitvavo({
    'APIKEY': '<APIKEY>',
    'APISECRET': '<APISECRET>',
    'RESTURL': 'https://api.bitvavo.com/v2',
    'WSURL': 'wss://ws.bitvavo.com/v2/',
    'ACCESSWINDOW': 10000,
    'DEBUGGING': False
  })
  testREST(bitvavo)
  testWebsockets(bitvavo)

def testREST(bitvavo):
  limit = bitvavo.getRemainingLimit()
  print('Remaining ratelimit is', limit)

  response = bitvavo.time()
  print(response)

  # response = bitvavo.markets({})
  # for market in response:
  #   print(json.dumps(market, indent=2))

  # response = bitvavo.assets({})
  # for asset in response:
  #   print(json.dumps(asset, indent=2))

  # response = bitvavo.book('BTC-EUR', {})
  # print(json.dumps(response, indent=2))

  # response = bitvavo.publicTrades('BTC-EUR', {})
  # for trade in response:
  #   print(json.dumps(trade, indent=2))

  # Timestamp: candle[0], open: candle[1], high: candle[2], low: candle[3], close: candle[4], volume: candle[5]
  # response = bitvavo.candles('BTC-EUR', '1h', {})
  # for candle in response:
  #   print(json.dumps(candle, indent=2))
  
  # response = bitvavo.tickerPrice({})
  # print(json.dumps(response, indent=2))

  # response = bitvavo.tickerBook({})
  # for market in response:
  #   print(json.dumps(market, indent=2))

  # response = bitvavo.ticker24h({})
  # for market in response:
  #   print(json.dumps(market, indent=2))

  # response = bitvavo.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '0.1', 'price': '2000' })
  # print(json.dumps(response, indent=2))

  # response = bitvavo.placeOrder('BTC-EUR', 'sell', 'stopLoss', { amount: '0.1', 'triggerType': 'price', 'triggerReference': 'lastTrade', 'triggerAmount': '5000' })
  # print(json.dumps(response, indent=2))

  # response = bitvavo.getOrder('BTC-EUR', 'dd055772-0f02-493c-a049-f4356fa0d221')
  # print(json.dumps(response, indent=2))

  # response = bitvavo.updateOrder("BTC-EUR", "dd055772-0f02-493c-a049-f4356fa0d221", { "amount": "0.2" })
  # print(json.dumps(response, indent=2))

  # response = bitvavo.cancelOrder('BTC-EUR', 'dd055772-0f02-493c-a049-f4356fa0d221')
  # print(json.dumps(response, indent=2))

  # response = bitvavo.getOrders('BTC-EUR', {})
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.cancelOrders({ 'market': 'BTC-EUR' })
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.ordersOpen({})
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.trades('BTC-EUR', {})
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.account()
  # print(json.dumps(response, indent=2))

  # response = bitvavo.balance({})
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.depositAssets('BTC')
  # print(json.dumps(response, indent=2))

  # response = bitvavo.withdrawAssets('BTC', '1', 'BitcoinAddress', {})
  # print(json.dumps(response, indent=2))

  # response = bitvavo.depositHistory({})
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.withdrawalHistory({})
  # for item in response:
  #   print(json.dumps(item, indent=2))

# Normally you would define a seperate callback for every function.
def callback(response):
  print("Callback:", json.dumps(response, indent=2))

def errorCallback(error):
  print("Error callback:", json.dumps(error, indent=2))

def testWebsockets(bitvavo):
  websocket = bitvavo.newWebsocket()
  websocket.setErrorCallback(errorCallback)

  # websocket.time(callback)
  # websocket.markets({}, callback)
  # websocket.assets({}, callback)

  # websocket.book('BTC-EUR', { }, callback)
  # websocket.publicTrades('BTC-EUR', {}, callback)
  # websocket.candles('BTC-EUR', '1h', {}, callback)
  
  # websocket.ticker24h({}, callback)
  # websocket.tickerPrice({}, callback)
  # websocket.tickerBook({}, callback)

  # websocket.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '1', 'price': '3000' }, callback)
  # websocket.getOrder('BTC-EUR', '6d0dffa7-07fe-448e-9928-233821e7cdb5', callback)
  # websocket.updateOrder('BTC-EUR', '6d0dffa7-07fe-448e-9928-233821e7cdb5', { 'amount': '1.1' }, callback)
  # websocket.cancelOrder('BTC-EUR', '6d0dffa7-07fe-448e-9928-233821e7cdb5', callback)
  # websocket.getOrders('BTC-EUR', {}, callback)
  # websocket.cancelOrders({ 'market': 'BTC-EUR' }, callback)
  # websocket.ordersOpen({}, callback)

  # websocket.trades('BTC-EUR', {}, callback)

  # websocket.account(callback)
  # websocket.balance({}, callback)
  # websocket.depositAssets('BTC', callback)
  # websocket.withdrawAssets('BTC', '1', 'BitcoinAddress', {}, callback)
  # websocket.depositHistory({}, callback)
  # websocket.withdrawalHistory({}, callback)

  # websocket.subscriptionTicker('BTC-EUR', callback)
  # websocket.subscriptionTicker24h('BTC-EUR', callback)
  # websocket.subscriptionAccount('BTC-EUR', callback)
  # websocket.subscriptionCandles('BTC-EUR', '1h', callback)
  # websocket.subscriptionTrades('BTC-EUR', callback)
  # websocket.subscriptionBookUpdate('BTC-EUR', callback)

  # websocket.subscriptionBook('BTC-EUR', callback)
  limit = bitvavo.getRemainingLimit()
  try:
    while(limit > 0):
      time.sleep(0.5)
      limit = bitvavo.getRemainingLimit()
  except KeyboardInterrupt:
    websocket.closeSocket()

if __name__ == '__main__':
  main()