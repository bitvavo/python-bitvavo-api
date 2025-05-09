from datetime import datetime, timezone
from python_bitvavo_api.bitvavo import Bitvavo
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
    'APIKEY': 'a2c2c44fa4457addbec6b08f264febb0fd102be0d08cd989dd75fb6f1e127385',
    'APISECRET': 'fd53003af7bd886c5ed0b6630a559e52cdc53c38d19276d27d6ef97158e2c6f35e771a0403315d8e056400d5c016e2123e77d79e4b239d43112cb478811382d4',
    'RESTURL': 'https://api.dev.vavo.dev/v2',
    'WSURL': 'wss://edge.dev.internal.vavo.dev/exchange/wsg/v2'
  })
  # testREST(bitvavo)
  testWebsockets(bitvavo)

def testREST(bitvavo):
  limit = bitvavo.getRemainingLimit()
  print('Remaining ratelimit is', limit)

  response = bitvavo.time()
  print(response)

  # response = bitvavo.markets()
  # for market in response:
  #   print(json.dumps(market, indent=2))

  # response = bitvavo.assets()
  # for asset in response:
  #   print(json.dumps(asset, indent=2))

  # response = bitvavo.book('BTC-EUR')
  # print(json.dumps(response, indent=2))

  # response = bitvavo.publicTrades('BTC-EUR')
  # for trade in response:
  #   print(json.dumps(trade, indent=2))

  # Timestamp: candle[0], open: candle[1], high: candle[2], low: candle[3], close: candle[4], volume: candle[5]
  # candles = bitvavo.candles('BTC-EUR', '15m')
  # candles = bitvavo.candles('BTC-EUR', '15m', limit=10)
  # candles = bitvavo.candles('BTC-EUR', '15m', start=datetime(year=2024, month=1, day=1, hour=0, tzinfo=timezone.utc), end=datetime(year=2024, month=1, day=1, hour=1, tzinfo=timezone.utc))
  # for candle in candles:
  #   print('Timestamp', candle[0], ' open', candle[1], ' high', candle[2], ' low', candle[3], ' close', candle[4], ' volume', candle[5])

  # response = bitvavo.tickerPrice({})
  # print(json.dumps(response, indent=2))

  # response = bitvavo.tickerBook({})
  # for market in response:
  #   print(json.dumps(market, indent=2))

  # response = bitvavo.ticker24h({})
  # for market in response:
  #   print(json.dumps(market, indent=2))

  response = bitvavo.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '0.1', 'price': '80000', 'operatorId': 1000 })
  response = bitvavo.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '0.1', 'price': '80000', 'operatorId': 1000 })
  response = bitvavo.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '0.1', 'price': '80000', 'operatorId': 1000 })
  print(json.dumps(response, indent=2))

  # response = bitvavo.placeOrder('BTC-EUR', 'sell', 'stopLoss', { amount: '0.1', 'triggerType': 'price', 'triggerReference': 'lastTrade', 'triggerAmount': '5000' })
  # print(json.dumps(response, indent=2))

  # response = bitvavo.getOrder('BTC-EUR', 'dd055772-0f02-493c-a049-f4356fa0d221')
  # print(json.dumps(response, indent=2))

  # time.sleep(5)
  orderId = response['orderId']
  # print(orderId)
  # response = bitvavo.updateOrder("BTC-EUR", response['orderId'], { "amount": "0.2", 'operatorId': 1001  })
  # print(json.dumps(response, indent=2))

  # response = bitvavo.cancelOrder('BTC-EUR', orderId, 1002)
  # print(json.dumps(response, indent=2))

  # response = bitvavo.getOrders('BTC-EUR')
  # for item in response:
  #   print(json.dumps(item, indent=2))

  response = bitvavo.cancelOrders({ 'market': 'BTC-EUR', 'operatorId': 1003 })
  for item in response:
    print(json.dumps(item, indent=2))

  # response = bitvavo.ordersOpen()
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.trades('BTC-EUR')
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.account()
  # print(json.dumps(response, indent=2))

  # response = bitvavo.balance()
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.depositAssets('BTC')
  # print(json.dumps(response, indent=2))

  # response = bitvavo.withdrawAssets('BTC', '1', 'BitcoinAddress', {})
  # print(json.dumps(response, indent=2))

  # response = bitvavo.depositHistory()
  # for item in response:
  #   print(json.dumps(item, indent=2))

  # response = bitvavo.withdrawalHistory()
  # for item in response:
  #   print(json.dumps(item, indent=2))

# Normally you would define a separate callback for every function.

orderId = None
def callback(response):
  dumps = json.dumps(response, indent=2)
  global orderId
  orderId = response.get('orderId')
  print("Callback:", dumps)

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

  websocket.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '1', 'price': '80000', 'operatorId': 1001 }, callback)
  # websocket.getOrder('BTC-EUR', '6d0dffa7-07fe-448e-9928-233821e7cdb5', callback)
  time.sleep(2)
  print(orderId)
  websocket.updateOrder('BTC-EUR', orderId, { 'amount': '1.1', 'operatorId': 1002 }, callback)
  # websocket.cancelOrder('BTC-EUR', orderId, callback, 1003)
  # websocket.getOrders('BTC-EUR', {}, callback)
  websocket.cancelOrders({ 'market': 'BTC-EUR', 'operatorId': 1004 }, callback)
  # websocket.ordersOpen({}, callback)

  # websocket.trades('BTC-EUR', {}, callback)

  # websocket.account(callback)
  # websocket.fees(callback)
  # websocket.fees("BTC-EUR", callback)
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
