
<table cellspacing="0" cellpadding="0" border="0" >
	<tr>
		<td>
			<table cellspacing="3" border="0">
				<tr>
					<td><a href="https://bitvavo.com"><img src="./assets/bitvavo-mark-square-blue.svg" width="100" title="Bitvavo Logo"></td>
					<td><h1>Bitvavo SDK for Python</h1></td>
				</tr>
			</table>
		</td>
	</tr>
</table>

Crypto starts with Bitvavo. You use Bitvavo SDK for Python to buy, sell, and store over 200 digital assets on Bitvavo from inside your own app. 

To trade and execute your advanced trading strategies, Bitvavo SDK for Python is a wrapper that enables you to easily call every endpoint in [Bitvavo API](https://docs.bitvavo.com/).

- [Prerequisites](#prerequisites) - what you need to start developing with Bitvavo SDK for Python.
- [Get started](#get-started) - rapidy create an app and start trading with Bitvavo. 
- [API reference](#api-reference) - in-depth information about Bitvavo SDK for Python

This page shows you how to use Bitvavo SDK for Python with websockets. For REST, see [Readme-rest](./README-REST.md).

## Prerequisites

To start programming with Bitvavo SDK for Python you need:

- [Python3](https://www.python.org/downloads/) installed on your development environment

   If you are working on MacOS, ensure that that you have installed SSH certificates:
   ```terminal
    open /Applications/Python\ 3.12/Install\ Certificates.command
    open /Applications/Python\ 3.12/Update\ Shell\ Profile.command
    ```
- A Python app. Use your favorite IDE, or run from the command line
- An [API key and secret](https://support.bitvavo.com/hc/en-us/articles/4405059841809) associated with your Bitvavo account

  You control the actions your app can do using the rights you assign to the API key. Possible rights are:
  - **View**: retrieve information about your balance, account, deposit and withdrawals.
  - **Trade**: place, update, view and cancel orders.
  - **Withdraw**: withdraw funds.

       Best practice is to not grant his privilage, withdrawals using the API do not require 2FA and e-mail confirmation.

## Get started

Want to quickly make a first app? Here we go: 

1. **Install Bitvavo SDK for Python**  

    In your Python app, add [Bitvavo SDK for Python](https://github.com/bitvavo/python-bitvavo-api) from [pypi.org](https://pypi.org/project/python-bitvavo-api/):
     ```terminal
     python -m pip install python_bitvavo_api
     ```
1. **Create a simple Bitvavo implementation**

    Add the following code to a new file in your app:

    ```python
    # Import Bitvavo SDK for Python
    from python_bitvavo_api.bitvavo import Bitvavo
    import json
    import time
    
    
    # Use this class to connect to Bitvavo and make your first calls
    # Add trading strategies to implement your business logic.
    class bitvavo_implementation:
        api_key = "<Replace with your your API key from Bitvavo Dashboard>"
        api_secret = "<Replace with your API secrete from Bitvavo Dashboard>"
        bitvavo_engine = None
        bitvavo_socket = None
    
        # Connect securely to Bitvavo, create the websocket and error callbacks
        def __init__(self):
            self.bitvavo_engine = Bitvavo({
                'APIKEY': self.api_key,
                'APISECRET': self.api_secret
            })
            self.bitvavo_socket = self.bitvavo_engine.newWebsocket()
            self.bitvavo_socket.setErrorCallback(self.error_callback)
    
        # Handle errors
        def error_callback(self, error):
            print("Errors:", json.dumps(error, indent=2))
    
        # Retrieve the data you need from Bitvavo in order to implement your
        # Trading logic. Use multiple workflows to return data to your
        # Callbacks
        def a_trading_strategy(self):
            self.bitvavo_socket.ticker24h({}, self.a_trading_strategy_callback)
            # You can also filter the ticker to retrieve specific markets only. 
    
        # In your app you analyse data returned by the workflow, then make
        # calls to Bitvavo to respond to market conditions
        def a_trading_strategy_callback(self, response):
            # Iterate through the
            for market in response:
                match market["market"]:
                   case "A market":
                        print("Check data against your trading strategy. For example, the bid is: ", market["bid"] )
                        # Implement calculations for your trading logic
                        # If they are positive, place an order: For example:
                        # self.bitvavo_socket.placeOrder("A market",
                        #                               'buy',
                        #                               'limit',
                        #                               { 'amount': '1', 'price': '00001' },
                        #                               self.order_placed_callback)
                   case "a different market":
                        print("Implement a different strategy for this market")
    
    
        def order_placed_callback(self, response):
            print("Order placed:", json.dumps(response, indent=2))
            # Add your business logic to handle orders
    
    
        # Sockets are fast, but asynchronous. Keep the socket open while you are
        # trading.
        def wait_and_close(self):
            limit = self.bitvavo_engine.getRemainingLimit()
            try:
                while (limit > 0):
                    time.sleep(0.5)
                    limit = self.bitvavo_engine.getRemainingLimit()
            except KeyboardInterrupt:
                self.bitvavo_socket.closeSocket()
    
    
    # Shall I re-explain main? Naaaaaaaaaa.
    if __name__ == '__main__':
        bvavo = bitvavo_implementation()
        bvavo.a_trading_strategy()
        bvavo.wait_and_close()
    ```
1. **Add security information**

    Replace the values of  `api_key` and `api_secret` with your credentials from [Bitvavo Dashboard](https://account.bitvavo.com/user/api).
    
    You must supply your security information to trade on Bitvavo and see your account details. You can retrieve public information such as available markets, assets and current market without 
    supplying your key and secret. However, Bitvavo returns an error. 

1. **Run your app**

    - Command line warriors: `python3 <filename>`.
    - IDE heroes: press the big green button.
 
Your app connects to Bitvavo and returns a list the latest trade price for each market. The callback cycles through the 
market data so you can implement your trading logic. 

## API reference

This is the python wrapper for the Bitvavo API. This project can be used to build your own projects which interact with the Bitvavo platform. Every function available on the API can be called through a REST request or over websockets. For info on the specifics of every parameter consult the [Bitvavo API documentation](https://docs.bitvavo.com/)

* [General](#general)
  * [Rate limiting](#rate-limiting)
  * [REST requests](#rest-requests) 
  * [Time](#get-time)
  * [Markets](#get-markets)
  * [Assets](#get-assets)
* [Public market data](#public-market-data)
  * [Book](#get-book-per-market)
  * [Public Trades](#get-trades-per-market)
  * [Candles](#get-candles-per-market)
  * [Price Ticker](#get-price-ticker)
  * [Book Ticker](#get-book-ticker)
  * [24 Hour Ticker](#get-24-hour-ticker)
* [Private trading data](#private-trading-data)
  * [Place Order](#place-order)
  * [Update Order](#update-order)
  * [Get Order](#get-order)
  * [Cancel Order](#cancel-order)
  * [Get Orders](#get-orders)
  * [Cancel Orders](#cancel-orders)
  * [Orders Open](#get-orders-open)
  * [Trades](#get-trades)
  * [Account](#get-account)
  * [Balance](#get-balance)
  * [Deposit](#deposit-assets)
  * [Withdraw](#withdraw-assets)
  * [Deposit History](#get-deposit-history)
  * [Withdrawal History](#get-withdrawal-history)
* [Subscriptions](#subscriptions)
  * [Ticker Subscription](#ticker-subscription)
  * [Ticker 24 Hour Subscription](#ticker-24-hour-subscription)
  * [Account Subscription](#account-subscription)
  * [Candles Subscription](#candles-subscription)
  * [Trades Subscription](#trades-subscription)
  * [Book Subscription](#book-subscription)
  * [Book subscription with local copy](#book-subscription-with-local-copy)

### General

#### Rate limiting

Bitvavo uses a weight based rate limiting system. Your app is limited to 1000 weight points per IP or API key per 
minute. When you make a call to Bitvavo API, your remaining weight points are returned in the header of each REST request. 

Websocket functions do not return your returning weight points, you track your remaining weight points with a call to:
```
limit = bitvavo.getRemainingLimit()
```

If you make more requests than permitted by the weight limit, your IP or API key is banned. 

The rate weighting for each endpoint is supplied in the [Bitvavo API documentation](https://docs.bitvavo.com/).

#### REST requests

For all functions, required parameters are passed as separate values, optional parameters are passed as a dictionary; 
return parameters are in dictionary format such that `response['<key>'] = '<value>'`.  Only when [placing orders](#place-order) some of the optional parameters are required, since a limit order requires more information than a market order. 

#### Get time
```python
response = bitvavo.time()
print(response)
```
<details>
 <summary>View Response</summary>

```python
{
  "time": 1543397021396
}
```
</details>

### Public market data

#### Get time
```python
websocket.time(ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "time": 1543397021396
}
```
</details>

#### Get markets
```python
# options: market
websocket.markets({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "market": "ADA-BTC",
  "status": "trading",
  "base": "ADA",
  "quote": "BTC",
  "pricePrecision": 5,
  "minOrderInBaseAsset": "100",
  "minOrderInQuoteAsset": "0.001",
  "orderTypes": [
    "market",
    "limit"
  ]
}
{
  "market": "ADA-EUR",
  "status": "trading",
  "base": "ADA",
  "quote": "EUR",
  "pricePrecision": 5,
  "minOrderInBaseAsset": "100",
  "minOrderInQuoteAsset": "10",
  "orderTypes": [
    "market",
    "limit"
  ]
}
{
  "market": "AE-BTC",
  "status": "trading",
  "base": "AE",
  "quote": "BTC",
  "pricePrecision": 5,
  "minOrderInBaseAsset": "10",
  "minOrderInQuoteAsset": "0.001",
  "orderTypes": [
    "market",
    "limit"
  ]
}
{
  "market": "AE-EUR",
  "status": "trading",
  "base": "AE",
  "quote": "EUR",
  "pricePrecision": 5,
  "minOrderInBaseAsset": "10",
  "minOrderInQuoteAsset": "10",
  "orderTypes": [
    "market",
    "limit"
  ]
}
...
```
</details>

#### Get assets
```python
# options: symbol
websocket.assets({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "symbol": "ADA",
    "name": "Cardano",
    "decimals": 6,
    "depositFee": "0",
    "depositConfirmations": 20,
    "depositStatus": "OK",
    "withdrawalFee": "0.2",
    "withdrawalMinAmount": "0.2",
    "withdrawalStatus": "OK",
    "networks": [
      "Mainnet"
    ],
    "message": ""
  },
  {
    "symbol": "AE",
    "name": "Aeternity",
    "decimals": 8,
    "depositFee": "0",
    "depositConfirmations": 30,
    "depositStatus": "OK",
    "withdrawalFee": "2",
    "withdrawalMinAmount": "2",
    "withdrawalStatus": "OK",
    "networks": [
      "Mainnet"
    ],
    "message": ""
  },
  {
    "symbol": "AION",
    "name": "Aion",
    "decimals": 8,
    "depositFee": "0",
    "depositConfirmations": 0,
    "depositStatus": "",
    "withdrawalFee": "3",
    "withdrawalMinAmount": "3",
    "withdrawalStatus": "",
    "networks": [
      "Mainnet"
    ],
    "message": ""
  },
  {
    "symbol": "ANT",
    "name": "Aragon",
    "decimals": 8,
    "depositFee": "0",
    "depositConfirmations": 30,
    "depositStatus": "OK",
    "withdrawalFee": "2",
    "withdrawalMinAmount": "2",
    "withdrawalStatus": "OK",
    "networks": [
      "Mainnet"
    ],
    "message": ""
  },
  ...
]
```
</details>

#### Get book per market
```python
# options: depth
websocket.book('BTC-EUR', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "market": "BTC-EUR",
  "nonce": 26393,
  "bids": [
    [
      "3008.8",
      "1.47148675"
    ],
    [
      "3008.3",
      "1.10515032"
    ],
    [
      "3007.7",
      "1.38627613"
    ],
    [
      "3007.2",
      "0.72343843"
    ],
    [
      "3006.7",
      "0.96668815"
    ],
    [
      "3006.2",
      "3.50846635"
    ],
    ...
  ],
  "asks": [
    [
      "3009.2",
      "2.74009412"
    ],
    [
      "3011.3",
      "3.03788636"
    ],
    [
      "3013.1",
      "3.91270989"
    ],
    [
      "3015.1",
      "4.33891895"
    ],
    [
      "3016",
      "1.34888815"
    ],
    [
      "3016.5",
      "1.95726644"
    ],
    ...
  ]
}
```
</details>

#### Get trades per market
```python
# options: limit, start, end, tradeIdFrom, tradeIdTo
websocket.publicTrades('BTC-EUR', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[ 
  {
    "id": "041689b3-cbb6-49ec-9964-2fb2d353dd1b",
    "timestamp": 1565672192018,
    "amount": "0.12735922",
    "price": "10147",
    "side": "sell"
  },
  {
    "id": "fb1712f2-e183-457c-b9e5-ff0d31fccd1f",
    "timestamp": 1565672192014,
    "amount": "0.08703703",
    "price": "10149",
    "side": "sell"
  },
  {
    "id": "b8cf5e20-65ca-4f45-a94c-44b7cb3952a5",
    "timestamp": 1565672192009,
    "amount": "0.0979994",
    "price": "10151",
    "side": "sell"
  },
  {
    "id": "d10cc7ec-a735-4d5c-8169-c3099f8b5003",
    "timestamp": 1565672144747,
    "amount": "0.01975188",
    "price": "10151",
    "side": "sell"
  }
  ...
]
```
</details>

#### Get candles per market
```python
# options: limit
websocket.candles('BTC-EUR', '1h', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  [
    1548669600000,
    "3012.9",
    "3015.8",
    "3000",
    "3012.9",
    "8"
  ],
  [
    1548669600000,
    "3012.9",
    "3015.8",
    "3000",
    "3012.9",
    "8"
  ],
  [
    1548669600000,
    "3012.9",
    "3015.8",
    "3000",
    "3012.9",
    "8"
  ],
  [
    1548417600000,
    "3124",
    "3125.1",
    "3124",
    "3124",
    "0.1"
  ],
  [
    1548237600000,
    "3143",
    "3143.3",
    "3141.1",
    "3143",
    "60.67250851"
  ],
  ...
]
```
</details>

#### Get price ticker
```python
# options: market
websocket.tickerPrice({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "market": "EOS-EUR",
    "price": "2.0142"
  },
  {
    "market": "XRP-EUR",
    "price": "0.27848"
  },
  {
    "market": "ETH-EUR",
    "price": "99.877"
  },
  {
    "market": "IOST-EUR",
    "price": "0.005941"
  },
  {
    "market": "BCH-EUR",
    "price": "106.57"
  },
  {
    "market": "BTC-EUR",
    "price": "3008.9"
  },
  {
    "market": "STORM-EUR",
    "price": "0.0025672"
  },
  {
    "market": "EOS-BTC",
    "price": "0.00066289"
  },
  ...
]
```
</details>

#### Get book ticker
```python
# options: market
websocket.tickerBook({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "market": "ZIL-BTC",
    "bid": "0.00000082",
    "ask": "0.00000083",
    "bidSize": "13822.00651664",
    "askSize": "5743.88893286"
  },
  {
    "market": "ZIL-EUR",
    "bid": "0.0082973",
    "ask": "0.0084058",
    "bidSize": "19586.15862762",
    "askSize": "19048.86640562"
  },
  {
    "market": "ZRX-BTC",
    "bid": "0.00001625",
    "ask": "0.00001629",
    "bidSize": "823.87743487",
    "askSize": "868.23901671"
  },
  {
    "market": "ZRX-EUR",
    "bid": "0.16443",
    "ask": "0.16498",
    "bidSize": "898.35016343",
    "askSize": "419.16696625"
  },
  ...
]
```
</details>

#### Get 24 hour ticker
```python
# options: market
websocket.ticker24h({}, timeCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "market": "XVG-EUR",
    "open": "0.0045692",
    "high": "0.0045853",
    "low": "0.0043599",
    "last": "0.0044047",
    "volume": "594786.9689017",
    "volumeQuote": "2648.07",
    "bid": "0.0043493",
    "bidSize": "1561220.43836043",
    "ask": "0.004453",
    "askSize": "1457312.74672114",
    "timestamp": 1565684835077
  },
  {
    "market": "ZIL-EUR",
    "open": "0.0081178",
    "high": "0.0084196",
    "low": "0.0077389",
    "last": "0.0084071",
    "volume": "950455.78568402",
    "volumeQuote": "7687.71",
    "bid": "0.008294",
    "bidSize": "19593.90088084",
    "ask": "0.0084",
    "askSize": "19048.86640562",
    "timestamp": 1565684834952
  },
  {
    "market": "ZRX-EUR",
    "open": "0.1731",
    "high": "0.1731",
    "low": "0.16426",
    "last": "0.16477",
    "volume": "22486.29651877",
    "volumeQuote": "3727.45",
    "bid": "0.16436",
    "bidSize": "898.75082725",
    "ask": "0.16476",
    "askSize": "419.31541176",
    "timestamp": 1565684835335
  },
  ...
]
```
</details>

### Private

#### Place order
When placing an order, make sure that the correct optional parameters are set. For a limit order it is required to set both the amount and price. A market order is valid if either amount or amountQuote has been set.
```python
# optional parameters: limit:(amount, price, postOnly), market:(amount, amountQuote, disableMarketProtection),
#                      stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
#                      stopLossLimit/takeProfitLimit:(amount, price, postOnly, triggerType, triggerReference, triggerAmount)
#                      all orderTypes: timeInForce, selfTradePrevention, responseRequired
websocket.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '1', 'price': '3000' }, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
    "orderId": "5444f908-67c4-4c5d-a138-7e834b94360e",
    "market": "BTC-EUR",
    "created": 1548671550610,
    "updated": 1548671550610,
    "status": "new",
    "side": "buy",
    "orderType": "limit",
    "amount": "1",
    "amountRemaining": "1",
    "price": "3000",
    "onHold": "3007.5",
    "onHoldCurrency": "EUR",
    "filledAmount": "0",
    "filledAmountQuote": "0",
    "feePaid": "0",
    "feeCurrency": "EUR",
    "fills": [],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
}
```
</details>

#### Update order
When updating an order make sure that at least one of the optional parameters has been set. Otherwise nothing can be updated.
```python
# Optional parameters: limit:(amount, amountRemaining, price, timeInForce, selfTradePrevention, postOnly)
#          untriggered stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
#                      stopLossLimit/takeProfitLimit: (amount, price, postOnly, triggerType, triggerReference, triggerAmount)
websocket.updateOrder('BTC-EUR', '5444f908-67c4-4c5d-a138-7e834b94360e', { 'amount': '1.1' }, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
    "orderId": "5444f908-67c4-4c5d-a138-7e834b94360e",
    "market": "BTC-EUR",
    "created": 1548671550610,
    "updated": 1548671831685,
    "status": "new",
    "side": "buy",
    "orderType": "limit",
    "amount": "1.1",
    "amountRemaining": "1.1",
    "price": "3000",
    "onHold": "3308.25",
    "onHoldCurrency": "EUR",
    "filledAmount": "0",
    "filledAmountQuote": "0",
    "feePaid": "0",
    "feeCurrency": "EUR",
    "fills": [],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
}
```
</details>

#### Get order
```python
websocket.getOrder('BTC-EUR', '5444f908-67c4-4c5d-a138-7e834b94360e', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
    "orderId": "5444f908-67c4-4c5d-a138-7e834b94360e",
    "market": "BTC-EUR",
    "created": 1548671550610,
    "updated": 1548671550610,
    "status": "new",
    "side": "buy",
    "orderType": "limit",
    "amount": "1",
    "amountRemaining": "1",
    "price": "3000",
    "onHold": "3007.5",
    "onHoldCurrency": "EUR",
    "filledAmount": "0",
    "filledAmountQuote": "0",
    "feePaid": "0",
    "feeCurrency": "EUR",
    "fills": [],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
}
```
</details>

#### Cancel order
```python
websocket.cancelOrder('BTC-EUR', '5986db7b-8d6e-4577-8003-22f363fb3626', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "orderId": "5986db7b-8d6e-4577-8003-22f363fb3626"
}
```
</details>

#### Get orders
Returns the same as get order, but can be used to return multiple orders at once.
```python
# options: limit, start, end, orderIdFrom, orderIdTo
websocket.getOrders('BTC-EUR', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "orderId": "bad72641-7755-464c-8dcb-7c1d59b142ab",
    "market": "BTC-EUR",
    "created": 1548670024870,
    "updated": 1548670024870,
    "status": "partiallyFilled",
    "side": "buy",
    "orderType": "limit",
    "amount": "1",
    "amountRemaining": "0.5",
    "price": "3000",
    "onHold": "1504.5",
    "onHoldCurrency": "EUR",
    "filledAmount": "0.5",
    "filledAmountQuote": "1500",
    "feePaid": "3",
    "feeCurrency": "EUR",
    "fills": [
      {
        "id": "108c3633-0276-4480-a902-17a01829deae",
        "timestamp": 1548671992530,
        "amount": "0.5",
        "price": "3000",
        "taker": false,
        "fee": "3",
        "feeCurrency": "EUR",
        "settled": true
      }
    ],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
  },
  {
    "orderId": "da1d8330-d6b7-4753-800a-01ad510a679b",
    "market": "BTC-EUR",
    "created": 1548666570234,
    "updated": 1548666570234,
    "status": "filled",
    "side": "sell",
    "orderType": "limit",
    "amount": "0.1",
    "amountRemaining": "0",
    "price": "4000",
    "onHold": "0",
    "onHoldCurrency": "BTC",
    "filledAmount": "0.1",
    "filledAmountQuote": "400",
    "feePaid": "0.8",
    "feeCurrency": "EUR",
    "fills": [
      {
        "id": "79e4bf2f-4fac-4895-9bb2-a5c9c6e2ff3f",
        "timestamp": 1548666712071,
        "amount": "0.1",
        "price": "4000",
        "taker": false,
        "fee": "0.8",
        "feeCurrency": "EUR",
        "settled": true
      }
    ],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
  },
  ...
]
```
</details>

#### Cancel orders
Cancels all orders in a market. If no market is specified, all orders of an account will be canceled.
```python
# options: market
websocket.cancelOrders({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "orderId": "4f9a809b-859f-4d8d-97b3-037113cdf2d0"
  }, 
  {
    "orderId": "95313ae5-ad65-4430-a0fb-63591bbc337c".
  }, 
  {
    "orderId": "2465c3ab-5ae2-4d4d-bec7-345f51b3494d"
  },
  ...
]
```
</details>

#### Get orders open
Returns all orders which are not filled or canceled.
```python
# options: market
websocket.ordersOpen({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "orderId": "bad72641-7755-464c-8dcb-7c1d59b142ab",
    "market": "BTC-EUR",
    "created": 1548670024870,
    "updated": 1548670024870,
    "status": "partiallyFilled",
    "side": "buy",
    "orderType": "limit",
    "amount": "1",
    "amountRemaining": "0.5",
    "price": "3000",
    "onHold": "1504.5",
    "onHoldCurrency": "EUR",
    "filledAmount": "0.5",
    "filledAmountQuote": "1500",
    "feePaid": "3",
    "feeCurrency": "EUR",
    "fills": [
      {
        "id": "108c3633-0276-4480-a902-17a01829deae",
        "timestamp": 1548671992530,
        "amount": "0.5",
        "price": "3000",
        "taker": false,
        "fee": "3",
        "feeCurrency": "EUR",
        "settled": true
      }
    ],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
  },
  {
    "orderId": "7586d610-2732-4ee6-8516-bed18cfc853b",
    "market": "BTC-EUR",
    "created": 1548670088749,
    "updated": 1548670088749,
    "status": "new",
    "side": "buy",
    "orderType": "limit",
    "amount": "1",
    "amountRemaining": "1",
    "price": "3000",
    "onHold": "3007.5",
    "onHoldCurrency": "EUR",
    "filledAmount": "0",
    "filledAmountQuote": "0",
    "feePaid": "0",
    "feeCurrency": "EUR",
    "fills": [],
    "selfTradePrevention": "decrementAndCancel",
    "visible": true,
    "timeInForce": "GTC",
    "postOnly": false
  },
  ...
]
```
</details>

#### Get trades
Returns all trades within a market for this account.
```python
# options: limit, start, end, tradeIdFrom, tradeIdTo
websocket.trades('BTC-EUR', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "id": "108c3633-0276-4480-a902-17a01829deae",
    "timestamp": 1548671992530,
    "market": "BTC-EUR",
    "side": "buy",
    "amount": "0.5",
    "price": "3000",
    "taker": false,
    "fee": "3",
    "feeCurrency": "EUR",
    "settled": true
  },
  {
    "id": "79e4bf2f-4fac-4895-9bb2-a5c9c6e2ff3f",
    "timestamp": 1548666712071,
    "market": "BTC-EUR",
    "side": "sell",
    "amount": "0.1",
    "price": "4000",
    "taker": false,
    "fee": "0.8",
    "feeCurrency": "EUR",
    "settled": true
  },
  {
    "id": "102486d3-5b72-4fa2-89cf-84c934edb7ae",
    "timestamp": 1548666561486,
    "market": "BTC-EUR",
    "side": "sell",
    "amount": "0.1",
    "price": "4000",
    "taker": true,
    "fee": "1",
    "feeCurrency": "EUR",
    "settled": true
  },
  ...
]
```
</details>

#### Get account
Returns the fee tier for this account.
```python
websocket.account(ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "fees": {
    "taker": "0.0025",
    "maker": "0.0015",
    "volume": "100.00"
  }
}
```
</details>

#### Get balance
Returns the balance for this account.
```python
# options: symbol
websocket.balance({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "symbol": "EUR",
    "available": "2599.95",
    "inOrder": "2022.65"
  },
  {
    "symbol": "BTC",
    "available": "1.65437",
    "inOrder": "0.079398"
  },
  {
    "symbol": "ADA",
    "available": "4.8",
    "inOrder": "0"
  },
  {
    "symbol": "BCH",
    "available": "0.00952811",
    "inOrder": "0"
  },
  {
    "symbol": "BSV",
    "available": "0.00952811",
    "inOrder": "0"
  },
  ...
]
```
</details>

#### Deposit assets
Returns the address which can be used to deposit funds.
```python
websocket.depositAssets('BTC', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "address": "BitcoinAddress"
}
```
</details>

#### Withdraw assets
Can be used to withdraw funds from Bitvavo.
```python
# optional parameters: paymentId, internal, addWithdrawalFee
websocket.withdrawAssets('BTC', '1', 'BitcoinAddress', {}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "success": True,
  "symbol": "BTC",
  "amount": "1"
}
```
</details>

#### Get deposit history
Returns the deposit history of your account.
```python
# options: symbol, limit, start, end
websocket.depositHistory({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "timestamp": 1521550025000,
    "symbol": "EUR",
    "amount": "1",
    "fee": "0",
    "status": "completed",
    "address": "NL12RABO324234234"
  },
  {
    "timestamp": 1511873910000,
    "symbol": "BTC",
    "amount": "0.099",
    "fee": "0",
    "status": "completed",
    "txId": "0c6497e608212a516b8218674cb0ca04f65b67a00fe8bddaa1ecb03e9b029255"
  },
  ...
]
```
</details>

#### Get withdrawal history
Returns the withdrawal history of an account.
```python
# options: symbol, limit, start, end
websocket.withdrawalHistory({}, ownCallback)
```
<details>
 <summary>View Response</summary>

```python
[
  {
    "timestamp": 1548425559000,
    "symbol": "BTC",
    "amount": "0.09994",
    "fee": "0.00006",
    "status": "awaiting_processing",
    "address": "1CqtG5z55x7bYD5GxsAXPx59DEyujs4bjm"
  },
  {
    "timestamp": 1548409721000,
    "symbol": "EUR",
    "amount": "50",
    "fee": "0",
    "status": "completed",
    "address": "NL123BIM"
  },
  {
    "timestamp": 1537803091000,
    "symbol": "BTC",
    "amount": "0.01939",
    "fee": "0.00002",
    "status": "completed",
    "txId": "da2299c86fce67eb899aeaafbe1f81cf663a3850cf9f3337c92b2d87945532db",
    "address": "3QpyxeA7yWWsSURXEmuBBzHpxjqn7Rbyme"
  },
  ...
]
```
</details>

### Subscriptions

#### Ticker subscription
Sends an update every time the best bid, best ask or last price changed.
```python
websocket.subscriptionTicker('BTC-EUR', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "event": "ticker",
  "market": "BTC-EUR",
  "bestBid": "9286.9",
  "bestBidSize": "0.10705272",
  "bestAsk": "9287.6",
  "bestAskSize": "0.10990704",
  "lastPrice": "9335"
}
```
</details>

#### Ticker 24 hour subscription
Updated ticker24h objects are sent on this channel once per second. A ticker24h object is considered updated if one of the values besides timestamp has changed.
```python
websocket.subscriptionTicker24h('BTC-EUR', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "market": "BTC-EUR",
  "open": "10140",
  "high": "10216",
  "low": "10062",
  "last": "10119",
  "volume": "37.59541492",
  "volumeQuote": "381752.87",
  "bid": "10118",
  "bidSize": "0.07267404",
  "ask": "10119",
  "askSize": "0.09386124",
  "timestamp": 1565685285795
}
```
</details>

#### Account subscription
Sends an update whenever an event happens which is related to the account. These are ‘order’ events (create, update, cancel) or ‘fill’ events (a trade occurred).
```python
websocket.subscriptionAccount("BTC-EUR", ownCallback)
```
<details>
 <summary>View Response</summary>

```python
Fill:
{
  "event": "fill",
  "timestamp": 1548674189411,
  "market": "BTC-EUR",
  "orderId": "78fef2d4-6278-4f4b-ade9-1a1c438680e5",
  "fillId": "90d49d30-9d90-427d-ab4d-35d18c3356cb",
  "side": "buy",
  "amount": "0.03322362",
  "price": "3002.4",
  "taker": true,
  "fee": "0.249403312",
  "feeCurrency": "EUR"
}

Order:
{
  "event": "order",
  "orderId": "78fef2d4-6278-4f4b-ade9-1a1c438680e5",
  "market": "BTC-EUR",
  "created": 1548674189406,
  "updated": 1548674189406,
  "status": "filled",
  "side": "buy",
  "orderType": "market",
  "amountQuote": "100",
  "amountQuoteRemaining": "0.249403312",
  "onHold": "0",
  "onHoldCurrency": "EUR",
  "selfTradePrevention": "decrementAndCancel",
  "visible": false,
  "disableMarketProtection": false
}
```
</details>

#### Candles subscription
Sends an updated candle after each trade for the specified interval and market.
```python
websocket.subscriptionCandles('BTC-EUR', '1h', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "event": "candle",
  "market": "BTC-EUR",
  "interval": "1h",
  "candle": [
    [
      1548676800000,
      "2999.3",
      "2999.3",
      "2990.5",
      "2999.3",
      "11.15058838"
    ]
  ]
}
```
</details>

#### Trades subscription
Sends an update whenever a trade has happened on this market. For your own trades, please subscribe to account.
```python
websocket.subscriptionTrades('BTC-EUR', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "event": "trade",
  "timestamp": 1548677539543,
  "market": "BTC-EUR",
  "id": "d91bf798-e704-4f09-95f7-3444f8109346",
  "amount": "0.88114879",
  "price": "2992.2",
  "side": "buy"
}
```
</details>

#### Book subscription
Sends an update whenever the order book for this specific market has changed. A list of tuples ([price, amount]) are returned, where amount ‘0’ means that there are no more orders at this price. If you wish to maintain your own copy of the order book, consider using the next function.
```python
websocket.subscriptionBookUpdate('BTC-EUR', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "event": "book",
  "market": "BTC-EUR",
  "nonce": 14870,
  "bids": [
    [
      "2994.3",
      "0"
    ],
    [
      "2994.2",
      "0.00334147"
    ]
  ],
  "asks": []
}
```
</details>

#### Book subscription with local copy
This is a combination of get book per market and the book subscription which maintains a local copy. On every update to the order book, the entire order book is returned to the callback, while the book subscription will only return updates to the book.
```python
websocket.subscriptionBook('BTC-EUR', ownCallback)
```
<details>
 <summary>View Response</summary>

```python
{
  "bids": [
    [
      "2996.7",
      "0.36620062"
    ],
    [
      "2994.8",
      "0.04231826"
    ],
    [
      "2994.2",
      "0.16617026"
    ],
    [
      "2993.7",
      "0.23002489"
    ],
    ...
  ],
  "asks": [
    [
      "2998.6",
      "8.64251588"
    ],
    [
      "3001.2",
      "5.91405558"
    ],
    [
      "3002.4",
      "3.5765691"
    ],
    [
      "3003.9",
      "3.842524"
    ],
    ...
  ],
  "nonce": 21919,
  "market": "BTC-EUR"
}
```
</details>