
<table cellspacing="0" cellpadding="0" border="0" >
	<tr>
		<td>
			<table cellspacing="3" border="0">
				<tr>
					<td><a href="https://bitvavo.com"><img src="./assets/bitvavo-mark-square-blue.svg" width="100" title="Bitvavo Logo"/></td>
					<td><h1>Bitvavo SDK for Python</h1></td>
				</tr>
			</table>
		</td>
	</tr>
</table>

Crypto starts with Bitvavo. You use Bitvavo SDK for Python to buy, sell, and store over 200 digital assets on Bitvavo from inside your own app. 

To trade and execute your advanced trading strategies, Bitvavo SDK for Python is a wrapper that enables you to easily call every endpoint in [Bitvavo API](https://docs.bitvavo.com/).

- [Prerequisites](#prerequisites) - what you need to start developing with Bitvavo SDK for Python. 
- [API reference](#api-reference) - in-depth information about Bitvavo SDK for Python

This page gives reference information for REST calls made using Bitvavo SDK for Python.

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

       Best practice is to not grant his privilege, withdrawals using the API do not require 2FA and e-mail confirmation.

## API reference

This is the python wrapper for the Bitvavo API. This project can be used to build your own projects which interact with the Bitvavo platform. Every function available on the API can be called through a REST request or over websockets. For info on the specifics of every parameter consult the [Bitvavo API documentation](https://docs.bitvavo.com/)

* [General](#general)
  * [Rate limiting](#rate-limiting)
  * [REST requests](#rest-requests) 
  * [Time](#get-time)
  * [Markets](https://github.com/bitvavo/python-bitvavo-api#get-markets)
  * [Assets](https://github.com/bitvavo/python-bitvavo-api#get-assets)
* [Public market data](#public-market-data)
  * [Book](https://github.com/bitvavo/python-bitvavo-api#get-book-per-market)
  * [Public Trades](https://github.com/bitvavo/python-bitvavo-api#get-trades-per-market)
  * [Candles](https://github.com/bitvavo/python-bitvavo-api#get-candles-per-market)
  * [Price Ticker](https://github.com/bitvavo/python-bitvavo-api#get-price-ticker)
  * [Book Ticker](https://github.com/bitvavo/python-bitvavo-api#get-book-ticker)
  * [24 Hour Ticker](https://github.com/bitvavo/python-bitvavo-api#get-24-hour-ticker)
* [Private trading data](#private-trading-data)
  * [Place Order](https://github.com/bitvavo/python-bitvavo-api#place-order)
  * [Update Order](https://github.com/bitvavo/python-bitvavo-api#update-order)
  * [Get Order](https://github.com/bitvavo/python-bitvavo-api#get-order)
  * [Cancel Order](https://github.com/bitvavo/python-bitvavo-api#cancel-order)
  * [Get Orders](https://github.com/bitvavo/python-bitvavo-api#get-orders)
  * [Cancel Orders](https://github.com/bitvavo/python-bitvavo-api#cancel-orders)
  * [Orders Open](https://github.com/bitvavo/python-bitvavo-api#get-orders-open)
  * [Trades](https://github.com/bitvavo/python-bitvavo-api#get-trades)
  * [Account](https://github.com/bitvavo/python-bitvavo-api#get-account)
  * [Balance](https://github.com/bitvavo/python-bitvavo-api#get-balance)
  * [Deposit Assets](https://github.com/bitvavo/python-bitvavo-api#deposit-assets)
  * [Withdraw Assets](https://github.com/bitvavo/python-bitvavo-api#withdraw-assets)
  * [Deposit History](https://github.com/bitvavo/python-bitvavo-api#get-deposit-history)
  * [Withdrawal History](https://github.com/bitvavo/python-bitvavo-api#get-withdrawal-history)

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
return parameters are in dictionary format such that `response['<key>'] = '<value>'`.  Only when [placing orders](https://github.com/bitvavo/python-bitvavo-api#place-order) some of the optional parameters are required, since a limit order requires more information than a market order. 

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

#### Get markets
```python
# options: market
response = bitvavo.markets({})
print(response)
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
response = bitvavo.assets({})
print(response)
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

### Market Data

#### Get book per market
```python
# options: depth
response = bitvavo.book('BTC-EUR', {})
print(response)
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
response = bitvavo.publicTrades('BTC-EUR', {})
print(response)
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
# options: limit, start, end
response = bitvavo.candles('BTC-EUR', '1h', {})
print(response)
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
response = bitvavo.tickerPrice({})
print(response)
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
response = bitvavo.tickerBook({})
print(response)
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
response = bitvavo.ticker24h({})
print(response)
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

### Private trading data

#### Place order
When placing an order, make sure that the correct optional parameters are set. For a limit order it is required to set both the amount and price. A market order is valid if either amount or amountQuote is set.
```python
# optional parameters: limit:(amount, price, postOnly), market:(amount, amountQuote, disableMarketProtection),
#                      stopLoss/takeProfit:(amount, amountQuote, disableMarketProtection, triggerType, triggerReference, triggerAmount)
#                      stopLossLimit/takeProfitLimit:(amount, price, postOnly, triggerType, triggerReference, triggerAmount)
#                      all orderTypes: timeInForce, selfTradePrevention, responseRequired
response = bitvavo.placeOrder('BTC-EUR', 'buy', 'limit', { 'amount': '1', 'price': '3000' })
print(response)
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
response = bitvavo.updateOrder('BTC-EUR', '5444f908-67c4-4c5d-a138-7e834b94360e', { 'amount': '1.1' })
print(response)
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
response = bitvavo.getOrder('BTC-EUR', '5444f908-67c4-4c5d-a138-7e834b94360e')
print(response)
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
response = bitvavo.cancelOrder('BTC-EUR', '5986db7b-8d6e-4577-8003-22f363fb3626')
print(response)
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
response = bitvavo.getOrders('BTC-EUR', {})
print(response)
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
response = bitvavo.cancelOrders({})
print(response)
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
response = bitvavo.ordersOpen({})
print(response)
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
response = bitvavo.trades('BTC-EUR', {})
print(response)
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
response = bitvavo.account()
print(response)
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
response = bitvavo.balance({})
print(response)
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
response = bitvavo.depositAssets('BTC')
print(response)
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
response = bitvavo.withdrawAssets('BTC', '1', 'BitcoinAddress', {})
print(response)
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
response = bitvavo.depositHistory({})
print(response)
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
response = bitvavo.withdrawalHistory({})
print(response)
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




