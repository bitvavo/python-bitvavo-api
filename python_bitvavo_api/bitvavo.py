from threading import Timer
import requests
import time
import hmac
import hashlib
import json
import websocket
import threading
import os
import signal
import sys
import datetime

debugging = False

def debugToConsole(message):
  if(debugging):
    print(str(datetime.datetime.now().time())[:-7] + " DEBUG: " + message)

def errorToConsole(message):
  print(str(datetime.datetime.now().time())[:-7] + " ERROR: " + message)

def createSignature(timestamp, method, url, body, APISECRET):
  string = str(timestamp) + method + '/v2' + url
  if(len(body.keys()) != 0):
    string += json.dumps(body, separators=(',',':'))
  signature = hmac.new(APISECRET.encode('utf-8'), string.encode('utf-8'), hashlib.sha256).hexdigest()
  return signature

def createPostfix(options):
  params = []
  for key in options:
    params.append(key + '=' + str(options[key]))
  postfix = '&'.join(params)
  if(len(options) > 0):
    postfix = '?' + postfix
  return postfix

def asksCompare(a, b):
  if(a < b):
    return True
  return False

def bidsCompare(a, b):
  if(a > b):
    return True
  return False

def sortAndInsert(book, update, compareFunc):
  for updateEntry in update:
    entrySet = False
    for j in range(len(book)):
      bookItem = book[j]
      if compareFunc(float(updateEntry[0]), float(bookItem[0])):
        book.insert(j, updateEntry)
        entrySet = True
        break
      if float(updateEntry[0]) == float(bookItem[0]):
        if float(updateEntry[1]) > 0.0:
          book[j] = updateEntry
          entrySet = True
          break
        else:
          book.pop(j)
          entrySet = True
          break
    if not entrySet:
      book.append(updateEntry)
  return book

def processLocalBook(ws, message):
  if('action' in message):
    if(message['action'] == 'getBook'):
      market = message['response']['market']
      ws.localBook[market]['bids'] = message['response']['bids']
      ws.localBook[market]['asks'] = message['response']['asks']
      ws.localBook[market]['nonce'] = message['response']['nonce']
      ws.localBook[market]['market'] = market
  elif('event' in message):
    if(message['event'] == 'book'):
      market = message['market']

      if(message['nonce'] != ws.localBook[market]['nonce'] + 1):
        ws.makeLocalBook(market, ws.callbacks['localBookUser'][market])
        return
      ws.localBook[market]['bids'] = sortAndInsert(ws.localBook[market]['bids'], message['bids'], bidsCompare)
      ws.localBook[market]['asks'] = sortAndInsert(ws.localBook[market]['asks'], message['asks'], asksCompare)
      ws.localBook[market]['nonce'] = message['nonce']

  ws.callbacks['subscriptionBookUser'][market](ws.localBook[market])

class rateLimitThread (threading.Thread):
  def __init__(self, reset, bitvavo):
    self.timeToWait = reset
    self.bitvavo = bitvavo
    threading.Thread.__init__(self)

  def waitForReset(self, waitTime):
    time.sleep(waitTime)
    if (time.time() < self.bitvavo.rateLimitReset):
      self.bitvavo.rateLimitRemaining = 1000
      debugToConsole('Ban should have been lifted, resetting rate limit to 1000.')
    else:
      timeToWait = (self.bitvavo.rateLimitReset / 1000) - time.time()
      debugToConsole('Ban took longer than expected, sleeping again for', timeToWait, 'seconds.')
      self.waitForReset(timeToWait)

  def run(self):
    self.waitForReset(self.timeToWait)


class receiveThread (threading.Thread):
  def __init__(self, ws, wsObject):
    self.ws = ws
    self.wsObject = wsObject
    threading.Thread.__init__(self)

  def run(self):
    try:
      while(self.wsObject.keepAlive):
        self.ws.run_forever()
        self.wsObject.reconnect = True
        self.wsObject.authenticated = False
        time.sleep(self.wsObject.reconnectTimer)
        debugToConsole("we have just set reconnect to true and have waited for " + str(self.wsObject.reconnectTimer))
        self.wsObject.reconnectTimer = self.wsObject.reconnectTimer * 2
    except KeyboardInterrupt:
      debugToConsole("We caught keyboard interrupt in the websocket thread.")


class Bitvavo:
  def __init__(self, options = {}):
    self.base = "https://api.bitvavo.com/v2"
    self.wsUrl = "wss://ws.bitvavo.com/v2/"
    self.ACCESSWINDOW = None
    self.APIKEY = ''
    self.APISECRET = ''
    self.rateLimitRemaining = 1000
    self.rateLimitReset = 0
    global debugging
    debugging = False
    for key in options:
      if key.lower() == "apikey":
        self.APIKEY = options[key]
      elif key.lower() == "apisecret":
        self.APISECRET = options[key]
      elif key.lower() == "accesswindow":
        self.ACCESSWINDOW = options[key]
      elif key.lower() == "debugging":
        debugging = options[key]
      elif key.lower() == "resturl":
        self.base = options[key]
      elif key.lower() == "wsurl":
        self.wsUrl = options[key]
    if(self.ACCESSWINDOW == None):
      self.ACCESSWINDOW = 10000

  def getRemainingLimit(self):
    return self.rateLimitRemaining

  def updateRateLimit(self, response):
    if 'errorCode' in response:
      if (response['errorCode'] == 105):
        self.rateLimitRemaining = 0
        self.rateLimitReset = int(response['error'].split(' at ')[1].split('.')[0])
        timeToWait = (self.rateLimitReset / 1000) - time.time()
        if(not hasattr(self, 'rateLimitThread')):
          self.rateLimitThread = rateLimitThread(timeToWait, self)
          self.rateLimitThread.daemon = True
          self.rateLimitThread.start()
      # setTimeout(checkLimit, timeToWait)
    if ('bitvavo-ratelimit-remaining' in response):
      self.rateLimitRemaining = int(response['bitvavo-ratelimit-remaining'])
    if ('bitvavo-ratelimit-resetat' in response):
      self.rateLimitReset = int(response['bitvavo-ratelimit-resetat'])
      timeToWait = (self.rateLimitReset / 1000) - time.time()
      if(not hasattr(self, 'rateLimitThread')):
          self.rateLimitThread = rateLimitThread(timeToWait, self)
          self.rateLimitThread.daemon = True
          self.rateLimitThread.start()


  def publicRequest(self, url):
    debugToConsole("REQUEST: " + url)
    if(self.APIKEY != ''):
      now = int(time.time() * 1000)
      sig = createSignature(now, 'GET', url.replace(self.base, ''), {}, self.APISECRET)
      headers = {
        'Bitvavo-Access-Key': self.APIKEY,
        'Bitvavo-Access-Signature': sig,
        'Bitvavo-Access-Timestamp': str(now),
        'Bitvavo-Access-Window': str(self.ACCESSWINDOW)
      }
      r = requests.get(url, headers = headers)
    else:
      r = requests.get(url)
    if('error' in r.json()):
      self.updateRateLimit(r.json())
    else:
      self.updateRateLimit(r.headers)
    return r.json()

  def privateRequest(self, endpoint, postfix, body = {}, method = 'GET'):
    now = int(time.time() * 1000)
    sig = createSignature(now, method, (endpoint + postfix), body, self.APISECRET)
    url = self.base + endpoint + postfix
    headers = {
      'Bitvavo-Access-Key': self.APIKEY,
      'Bitvavo-Access-Signature': sig,
      'Bitvavo-Access-Timestamp': str(now),
      'Bitvavo-Access-Window': str(self.ACCESSWINDOW),
    }
    debugToConsole("REQUEST: " + url)
    if(method == 'GET'):
      r = requests.get(url, headers = headers)
    elif(method == 'DELETE'):
      r = requests.delete(url, headers = headers)
    elif(method == 'POST'):
      r = requests.post(url, headers = headers, json = body)
    elif(method == 'PUT'):
      r = requests.put(url, headers = headers, json = body)
    if('error' in r.json()):
      self.updateRateLimit(r.json())
    else:
      self.updateRateLimit(r.headers)
    return r.json()

  def time(self):
    return self.publicRequest((self.base + '/time'))

  # options: market
  def markets(self, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/markets' + postfix))

  # options: symbol
  def assets(self, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/assets' + postfix))

  # options: depth
  def book(self, symbol, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/' + symbol + '/book' + postfix))

  # options: limit, start, end, tradeIdFrom, tradeIdTo
  def publicTrades(self, symbol, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/' + symbol + '/trades' + postfix))

  # options: limit, start, end
  def candles(self, symbol, interval, options):
    options['interval'] = interval
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/' + symbol + '/candles' + postfix))

  # options: market
  def tickerPrice(self, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/ticker/price' + postfix))

  # options: market
  def tickerBook(self, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/ticker/book' + postfix))

  # options: market
  def ticker24h(self, options):
    postfix = createPostfix(options)
    return self.publicRequest((self.base + '/ticker/24h' + postfix))

  # optional body parameters: limit:(amount, price, postOnly), market:(amount, amountQuote, disableMarketProtection)
  #                           stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
  #                           stopLossLimit/takeProfitLimit:(amount, price, postOnly, triggerType, triggerReference, triggerAmount)
  #                           all orderTypes: timeInForce, selfTradePrevention, responseRequired
  def placeOrder(self, market, side, orderType, body):
    body['market'] = market
    body['side'] = side
    body['orderType'] = orderType
    return self.privateRequest('/order', '', body, 'POST')

  def getOrder(self, market, orderId):
    postfix = createPostfix({ 'market': market, 'orderId': orderId })
    return self.privateRequest('/order', postfix, {}, 'GET')

  # Optional parameters: limit:(amount, amountRemaining, price, timeInForce, selfTradePrevention, postOnly)
  #          untriggered stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
  #                      stopLossLimit/takeProfitLimit: (amount, price, postOnly, triggerType, triggerReference, triggerAmount)
  def updateOrder(self, market, orderId, body):
    body['market'] = market
    body['orderId'] = orderId
    return self.privateRequest('/order', '', body, 'PUT')

  def cancelOrder(self, market, orderId):
    postfix = createPostfix({ 'market': market, 'orderId': orderId})
    return self.privateRequest('/order', postfix, {}, 'DELETE')

  # options: limit, start, end, orderIdFrom, orderIdTo
  def getOrders(self, market, options):
    options['market'] = market
    postfix = createPostfix(options)
    return self.privateRequest('/orders', postfix, {}, 'GET')

  # options: market
  def cancelOrders(self, options):
    postfix = createPostfix(options)
    return self.privateRequest('/orders', postfix, {}, 'DELETE')

  # options: market
  def ordersOpen(self, options):
    postfix = createPostfix(options)
    return self.privateRequest('/ordersOpen', postfix, {}, 'GET')

  # options: limit, start, end, tradeIdFrom, tradeIdTo
  def trades(self, market, options):
    options['market'] = market
    postfix = createPostfix(options)
    return self.privateRequest('/trades', postfix, {}, 'GET')

  def account(self):
    return self.privateRequest('/account', '', {}, 'GET')

  # options: symbol
  def balance(self, options):
    postfix = createPostfix(options)
    return self.privateRequest('/balance', postfix, {}, 'GET')

  def depositAssets(self, symbol):
    postfix = createPostfix({ 'symbol': symbol })
    return self.privateRequest('/depositAssets', postfix, {}, 'GET')

  # optional body parameters: paymentId, internal, addWithdrawalFee
  def withdrawAssets(self, symbol, amount, address, body):
    body['symbol'] = symbol
    body['amount'] = amount
    body['address'] = address
    return self.privateRequest('/withdrawal', '', body, 'POST')

  # options: symbol, limit, start, end
  def depositHistory(self, options):
    postfix = createPostfix(options)
    return self.privateRequest('/depositHistory', postfix, {}, 'GET')

  # options: symbol, limit, start, end
  def withdrawalHistory(self, options):
    postfix = createPostfix(options)
    return self.privateRequest('/withdrawalHistory', postfix, {}, 'GET')

  def newWebsocket(self):
    return Bitvavo.websocket(self.APIKEY, self.APISECRET, self.ACCESSWINDOW, self.wsUrl, self)

  class websocket:
    def __init__(self, APIKEY, APISECRET, ACCESSWINDOW, WSURL, bitvavo):
      self.APIKEY = APIKEY
      self.APISECRET = APISECRET
      self.ACCESSWINDOW = ACCESSWINDOW
      self.wsUrl = WSURL
      self.open = False
      self.callbacks = {}
      self.keepAlive = True
      self.reconnect = False
      self.reconnectTimer = 0.1
      self.bitvavo = bitvavo

      self.subscribe()

    def subscribe(self):
      websocket.enableTrace(False)
      ws = websocket.WebSocketApp(self.wsUrl, 
                                on_message = self.on_message,
                                on_error = self.on_error,
                                on_close = self.on_close)
      self.ws = ws
      ws.on_open = self.on_open

      self.receiveThread = receiveThread(ws, self)
      self.receiveThread.daemon = True
      self.receiveThread.start()

      self.authenticated = False
      self.keepBookCopy = False
      self.localBook = {}

    def closeSocket(self):
      self.ws.close()
      self.keepAlive = False
      self.receiveThread.join()

    def waitForSocket(self, ws, message, private):
      if (not private and self.open) or (private and self.authenticated and self.open):
        return
      else:
        time.sleep(0.1)
        self.waitForSocket(ws, message, private)

    def doSend(self, ws, message, private = False):
      if(private and self.APIKEY == ''):
        errorToConsole('You did not set the API key, but requested a private function.')
        return
      self.waitForSocket(ws, message, private)
      ws.send(message)
      debugToConsole('SENT: ' + message)

    def on_message(ws, msg):
      debugToConsole('RECEIVED: ' + msg)
      msg = json.loads(msg)
      callbacks = ws.callbacks

      if('error' in msg):
        if (msg['errorCode'] == 105):
          ws.bitvavo.updateRateLimit(msg)
        if('error' in callbacks):
          callbacks['error'](msg)
        else:
          errorToConsole(msg)

      if('action' in msg):
        if(msg['action'] == 'getTime'):
          callbacks['time'](msg['response'])
        elif(msg['action'] == 'getMarkets'):
          callbacks['markets'](msg['response'])
        elif(msg['action'] == 'getAssets'):
          callbacks['assets'](msg['response'])
        elif(msg['action'] == 'getTrades'):
          callbacks['publicTrades'](msg['response'])
        elif(msg['action'] == 'getCandles'):
          callbacks['candles'](msg['response'])
        elif(msg['action'] == 'getTicker24h'):
          callbacks['ticker24h'](msg['response'])
        elif(msg['action'] == 'getTickerPrice'):
          callbacks['tickerPrice'](msg['response'])
        elif(msg['action'] == 'getTickerBook'):
          callbacks['tickerBook'](msg['response'])
        elif(msg['action'] == 'privateCreateOrder'):
          callbacks['placeOrder'](msg['response'])
        elif(msg['action'] == 'privateUpdateOrder'):
          callbacks['updateOrder'](msg['response'])
        elif(msg['action'] == 'privateGetOrder'):
          callbacks['getOrder'](msg['response'])
        elif(msg['action'] == 'privateCancelOrder'):
          callbacks['cancelOrder'](msg['response'])
        elif(msg['action'] == 'privateGetOrders'):
          callbacks['getOrders'](msg['response'])
        elif(msg['action'] == 'privateGetOrdersOpen'):
          callbacks['ordersOpen'](msg['response'])
        elif(msg['action'] == 'privateGetTrades'):
          callbacks['trades'](msg['response'])
        elif(msg['action'] == 'privateGetAccount'):
          callbacks['account'](msg['response'])
        elif(msg['action'] == 'privateGetBalance'):
          callbacks['balance'](msg['response'])
        elif(msg['action'] == 'privateDepositAssets'):
          callbacks['depositAssets'](msg['response'])
        elif(msg['action'] == 'privateWithdrawAssets'):
          callbacks['withdrawAssets'](msg['response'])
        elif(msg['action'] == 'privateGetDepositHistory'):
          callbacks['depositHistory'](msg['response'])
        elif(msg['action'] == 'privateGetWithdrawalHistory'):
          callbacks['withdrawalHistory'](msg['response'])
        elif(msg['action'] == 'privateCancelOrders'):
          callbacks['cancelOrders'](msg['response'])
        elif(msg['action'] == 'getBook'):
          market = msg['response']['market']
          if('book' in callbacks):
            callbacks['book'](msg['response'])
          if(ws.keepBookCopy):
            if(market in callbacks['subscriptionBook']):
              callbacks['subscriptionBook'][market](ws, msg)

      elif('event' in msg):
        if(msg['event'] == 'authenticate'):
          ws.authenticated = True
        elif(msg['event'] == 'fill'):
          market = msg['market']
          callbacks['subscriptionAccount'][market](msg)
        elif(msg['event'] == 'order'):
          market = msg['market']
          callbacks['subscriptionAccount'][market](msg)
        elif(msg['event'] == 'ticker'):
          market = msg['market']
          callbacks['subscriptionTicker'][market](msg)
        elif(msg['event'] == 'ticker24h'):
          for entry in msg['data']:
            callbacks['subscriptionTicker24h'][entry['market']](entry)
        elif(msg['event'] == 'candle'):
          market = msg['market']
          interval = msg['interval']
          callbacks['subscriptionCandles'][market][interval](msg)
        elif(msg['event'] == 'book'):
          market = msg['market']
          if('subscriptionBookUpdate' in callbacks):
            if(market in callbacks['subscriptionBookUpdate']):
              callbacks['subscriptionBookUpdate'][market](msg)
          if(ws.keepBookCopy):
            if(market in callbacks['subscriptionBook']):
              callbacks['subscriptionBook'][market](ws, msg)
        elif(msg['event'] == 'trade'):
          market = msg['market']
          if('subscriptionTrades' in callbacks):
            callbacks['subscriptionTrades'][market](msg)

    def on_error(ws, error):
      if('error' in callbacks):
        callbacks['error'](error)
      else:
        errorToConsole(error)

    def on_close(self):
      self.receiveThread.exit()
      debugToConsole('Closed Websocket.')

    def checkReconnect(self):
      if('subscriptionTicker' in self.callbacks):
        for market in self.callbacks['subscriptionTicker']:
          self.subscriptionTicker(market, self.callbacks['subscriptionTicker'][market])
      if('subscriptionTicker24h' in self.callbacks):
        for market in self.callbacks['subscriptionTicker24h']:
          self.subscriptionTicker(market, self.callbacks['subscriptionTicker24h'][market])
      if('subscriptionAccount' in self.callbacks):
        for market in self.callbacks['subscriptionAccount']:
          self.subscriptionAccount(market, self.callbacks['subscriptionAccount'][market])
      if('subscriptionCandles' in self.callbacks):
        for market in self.callbacks['subscriptionCandles']:
          for interval in self.callbacks['subscriptionCandles'][market]:
            self.subscriptionCandles(market, interval, self.callbacks['subscriptionCandles'][market][interval])
      if('subscriptionTrades' in self.callbacks):
        for market in self.callbacks['subscriptionTrades']:
          self.subscriptionTrades(market, self.callbacks['subscriptionTrades'][market])
      if('subscriptionBookUpdate' in self.callbacks):
        for market in self.callbacks['subscriptionBookUpdate']:
          self.subscriptionBookUpdate(market, self.callbacks['subscriptionBookUpdate'][market])
      if('subscriptionBookUser' in self.callbacks):
        for market in self.callbacks['subscriptionBookUser']:
          self.subscriptionBook(market, self.callbacks['subscriptionBookUser'][market])

    def on_open(self):
      now = int(time.time()*1000)
      self.open = True
      self.reconnectTimer = 0.5
      if(self.APIKEY != ''):
        self.doSend(self.ws, json.dumps({ 'window':str(self.ACCESSWINDOW), 'action': 'authenticate', 'key': self.APIKEY, 'signature': createSignature(now, 'GET', '/websocket', {}, self.APISECRET), 'timestamp': now }))
      if self.reconnect:
        debugToConsole("we started reconnecting", self.checkReconnect)
        thread = threading.Thread(target = self.checkReconnect)
        thread.start()

    def setErrorCallback(self,callback):
      self.callbacks['error'] = callback

    def time(self, callback):
      self.callbacks['time'] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'getTime' }))

    # options: market
    def markets(self, options, callback):
      self.callbacks['markets'] = callback
      options['action'] = 'getMarkets'
      self.doSend(self.ws, json.dumps(options))

    # options: symbol
    def assets(self, options, callback):
      self.callbacks['assets'] = callback
      options['action'] = 'getAssets'
      self.doSend(self.ws, json.dumps(options))

    # options: depth
    def book(self, market, options, callback):
      self.callbacks['book'] = callback
      options['market'] = market
      options['action'] = 'getBook'
      self.doSend(self.ws, json.dumps(options))

    # options: limit, start, end, tradeIdFrom, tradeIdTo
    def publicTrades(self, market, options, callback):
      self.callbacks['publicTrades'] = callback
      options['market'] = market
      options['action'] = 'getTrades'
      self.doSend(self.ws, json.dumps(options))

    # options: limit
    def candles(self, market, interval, options, callback):
      self.callbacks['candles'] = callback
      options['market'] = market
      options['interval'] = interval
      options['action'] = 'getCandles'
      self.doSend(self.ws, json.dumps(options))

    # options: market
    def ticker24h(self, options, callback):
      self.callbacks['ticker24h'] = callback
      options['action'] = 'getTicker24h'
      self.doSend(self.ws, json.dumps(options))

    # options: market
    def tickerPrice(self, options, callback):
      self.callbacks['tickerPrice'] = callback
      options['action'] = 'getTickerPrice'
      self.doSend(self.ws, json.dumps(options))

    # options: market
    def tickerBook(self, options, callback):
      self.callbacks['tickerBook'] = callback
      options['action'] = 'getTickerBook'
      self.doSend(self.ws, json.dumps(options))

    # optional body parameters: limit:(amount, price, postOnly), market:(amount, amountQuote, disableMarketProtection)
    #                           stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
    #                           stopLossLimit/takeProfitLimit:(amount, price, postOnly, triggerType, triggerReference, triggerAmount)
    #                           all orderTypes: timeInForce, selfTradePrevention, responseRequired
    def placeOrder(self, market, side, orderType, body, callback):
      self.callbacks['placeOrder'] = callback
      body['market'] = market
      body['side'] = side
      body['orderType'] = orderType
      body['action'] = 'privateCreateOrder'
      self.doSend(self.ws, json.dumps(body), True)

    def getOrder(self, market, orderId, callback):
      self.callbacks['getOrder'] = callback
      options = { 'action': 'privateGetOrder', 'market': market, 'orderId': orderId }
      self.doSend(self.ws, json.dumps(options), True)

    # Optional parameters: limit:(amount, amountRemaining, price, timeInForce, selfTradePrevention, postOnly)
    #          untriggered stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
    #                      stopLossLimit/takeProfitLimit: (amount, price, postOnly, triggerType, triggerReference, triggerAmount)
    def updateOrder(self, market, orderId, body, callback):
      self.callbacks['updateOrder'] = callback
      body['market'] = market
      body['orderId'] = orderId
      body['action'] = 'privateUpdateOrder'
      self.doSend(self.ws, json.dumps(body), True)

    def cancelOrder(self, market, orderId, callback):
      self.callbacks['cancelOrder'] = callback
      options = { 'action': 'privateCancelOrder', 'market': market, 'orderId': orderId }
      self.doSend(self.ws, json.dumps(options), True)

    # options: limit, start, end, orderIdFrom, orderIdTo
    def getOrders(self, market, options, callback):
      self.callbacks['getOrders'] = callback
      options['action'] = 'privateGetOrders'
      options['market'] = market
      self.doSend(self.ws, json.dumps(options), True)

    # options: market
    def cancelOrders(self, options, callback):
      self.callbacks['cancelOrders'] = callback
      options['action'] = 'privateCancelOrders'
      self.doSend(self.ws, json.dumps(options), True)

    # options: market
    def ordersOpen(self, options, callback):
      self.callbacks['ordersOpen'] = callback
      options['action'] = 'privateGetOrdersOpen'
      self.doSend(self.ws, json.dumps(options), True)

    # options: limit, start, end, tradeIdFrom, tradeIdTo
    def trades(self, market, options, callback):
      self.callbacks['trades'] = callback
      options['action'] = 'privateGetTrades'
      options['market'] = market
      self.doSend(self.ws, json.dumps(options), True)

    def account(self, callback):
      self.callbacks['account'] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'privateGetAccount' }), True)

    # options: symbol
    def balance(self, options, callback):
      options['action'] = 'privateGetBalance'
      self.callbacks['balance'] = callback
      self.doSend(self.ws, json.dumps(options), True)

    def depositAssets(self, symbol, callback):
      self.callbacks['depositAssets'] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'privateDepositAssets', 'symbol': symbol }), True)

    # optional body parameters: paymentId, internal, addWithdrawalFee
    def withdrawAssets(self, symbol, amount, address, body, callback):
      self.callbacks['withdrawAssets'] = callback
      body['action'] = 'privateWithdrawAssets'
      body['symbol'] = symbol
      body['amount'] = amount
      body['address'] = address
      self.doSend(self.ws, json.dumps(body), True)

    # options: symbol, limit, start, end
    def depositHistory(self, options, callback):
      self.callbacks['depositHistory'] = callback
      options['action'] = 'privateGetDepositHistory'
      self.doSend(self.ws, json.dumps(options), True)

    # options: symbol, limit, start, end
    def withdrawalHistory(self, options, callback):
      self.callbacks['withdrawalHistory'] = callback
      options['action'] = 'privateGetWithdrawalHistory'
      self.doSend(self.ws, json.dumps(options), True)

    def subscriptionTicker(self, market, callback):
      if 'subscriptionTicker' not in self.callbacks:
        self.callbacks['subscriptionTicker'] = {}
      self.callbacks['subscriptionTicker'][market] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'ticker', 'markets': [market] }] }))

    def subscriptionTicker24h(self, market, callback):
      if 'subscriptionTicker24h' not in self.callbacks:
        self.callbacks['subscriptionTicker24h'] = {}
      self.callbacks['subscriptionTicker24h'][market] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'ticker24h', 'markets': [market] }] }))

    def subscriptionAccount(self, market, callback):
      if 'subscriptionAccount' not in self.callbacks:
        self.callbacks['subscriptionAccount'] = {}
      self.callbacks['subscriptionAccount'][market] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'account', 'markets': [market] }] }), True)

    def subscriptionCandles(self, market, interval, callback):
      if 'subscriptionCandles' not in self.callbacks:
        self.callbacks['subscriptionCandles'] = {}
      if market not in self.callbacks['subscriptionCandles']:
        self.callbacks['subscriptionCandles'][market] = {}
      self.callbacks['subscriptionCandles'][market][interval] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'candles', 'interval': [interval], 'markets': [market] }] }))

    def subscriptionTrades(self, market, callback):
      if 'subscriptionTrades' not in self.callbacks:
        self.callbacks['subscriptionTrades'] = {}
      self.callbacks['subscriptionTrades'][market] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'trades', 'markets': [market] }] }))

    def subscriptionBookUpdate(self, market, callback):
      if 'subscriptionBookUpdate' not in self.callbacks:
        self.callbacks['subscriptionBookUpdate'] = {}
      self.callbacks['subscriptionBookUpdate'][market] = callback
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'book', 'markets': [market] }] })) 

    def subscriptionBook(self, market, callback):
      self.keepBookCopy = True
      if 'subscriptionBookUser' not in self.callbacks:
        self.callbacks['subscriptionBookUser'] = {}
      self.callbacks['subscriptionBookUser'][market] = callback
      if 'subscriptionBook' not in self.callbacks:
        self.callbacks['subscriptionBook'] = {}
      self.callbacks['subscriptionBook'][market] = processLocalBook
      self.doSend(self.ws, json.dumps({ 'action': 'subscribe', 'channels': [{ 'name': 'book', 'markets': [market] }] }))

      self.localBook[market] = {}
      self.doSend(self.ws, json.dumps({ 'action': 'getBook', 'market': market }))