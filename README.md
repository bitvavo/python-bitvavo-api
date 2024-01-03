
# Bitvavo SDK for Python

Crypto starts with Bitvavo. 
You use Bitvavo SDK for Python to buy, sell, and store over 200 digital assets on Bitvavo from inside your app. 

To trade and execute your advanced trading strategies, Bitvavo SDK for Python is a wrapper that enables you to easily call every endpoint in [Bitvavo API](https://docs.bitvavo.com/).

- [Prerequisites](#prerequisites) - what you need to start developing with Bitvavo SDK for Python
- [Get started](#get-started) - rapidly create an app and start trading with Bitvavo
- [About the SDK](#about-the-sdk) - general information about Bitvavo SDK for Python
- [API reference](https://docs.bitvavo.com/) - information on the specifics of every parameter

This page shows you how to use Bitvavo SDK for Python with WebSockets. 
For REST, see the [REST readme](docs/rest.md).

## Prerequisites

To start programming with Bitvavo SDK for Python you need:

- [Python3](https://www.python.org/downloads/) installed on your development environment

  If you are working on macOS, ensure that you have installed SSH certificates:
  ```terminal
  open /Applications/Python\ 3.12/Install\ Certificates.command
  open /Applications/Python\ 3.12/Update\ Shell\ Profile.command
  ```
- A Python app. Use your favorite IDE, or run from the command line
- An [API key and secret](https://support.bitvavo.com/hc/en-us/articles/4405059841809) associated with your Bitvavo account

  You control the actions your app can do using the rights you assign to the API key. 
  Possible rights are:
  + **View**: retrieve information about your balance, account, deposit and withdrawals
  + **Trade**: place, update, view and cancel orders
  + **Withdraw**: withdraw funds

    Best practice is to not grant this privilege, withdrawals using the API do not require 2FA and e-mail confirmation.

## Get started

Want to quickly make a trading app? Here you go: 

1. **Install Bitvavo SDK for Python**  

    In your Python app, add [Bitvavo SDK for Python](https://github.com/bitvavo/python-bitvavo-api) from [pypi.org](https://pypi.org/project/python-bitvavo-api/):
    ```terminal
    python -m pip install python_bitvavo_api
    ```

    If you installed from `test.pypi.com`, update the requests library: `pip install --upgrade  requests`.   


1. **Create a simple Bitvavo implementation**

    Add the following code to a new file in your app:

    ```python
    from python_bitvavo_api.bitvavo import Bitvavo
    import json
    import time
    
    # Use this class to connect to Bitvavo and make your first calls.
    # Add trading strategies to implement your business logic.
    class BitvavoImplementation:
        api_key = "<Replace with your your API key from Bitvavo Dashboard>"
        api_secret = "<Replace with your API secret from Bitvavo Dashboard>"
        bitvavo_engine = None
        bitvavo_socket = None
    
        # Connect securely to Bitvavo, create the WebSocket and error callbacks.
        def __init__(self):
            self.bitvavo_engine = Bitvavo({
                'APIKEY': self.api_key,
                'APISECRET': self.api_secret
            })
            self.bitvavo_socket = self.bitvavo_engine.newWebsocket()
            self.bitvavo_socket.setErrorCallback(self.error_callback)
    
        # Handle errors.
        def error_callback(self, error):
            print("Add your error message.")
            #print("Errors:", json.dumps(error, indent=2))
    
        # Retrieve the data you need from Bitvavo in order to implement your
        # trading logic. Use multiple workflows to return data to your
        # callbacks.
        def a_trading_strategy(self):
            self.bitvavo_socket.ticker24h({}, self.a_trading_strategy_callback)
    
        # In your app you analyse data returned by the trading strategy, then make
        # calls to Bitvavo to respond to market conditions.
        def a_trading_strategy_callback(self, response):
            # Iterate through the markets
            for market in response:
    
                match market["market"]:
                   case "ZRX-EUR":
                        print("Eureka, the latest bid for ZRX-EUR is: ", market["bid"] )
                        # Implement calculations for your trading logic.
                        # If they are positive, place an order: For example:
                        # self.bitvavo_socket.placeOrder("ZRX-EUR",
                        #                               'buy',
                        #                               'limit',
                        #                               { 'amount': '1', 'price': '00001' },
                        #                               self.order_placed_callback)
                   case "a different market":
                        print("do something else")
                   case _:
                        print("Not this one: ", market["market"])
    
    
    
        def order_placed_callback(self, response):
            # The order return parameters explain the quote and the fees for this trade.
            print("Order placed:", json.dumps(response, indent=2))
            # Add your business logic.
    
    
        # Sockets are fast, but asynchronous. Keep the socket open while you are
        # trading.
        def wait_and_close(self):
            # Bitvavo uses a weight based rate limiting system. Your app is limited to 1000 weight points per IP or
            # API key per minute. The rate weighting for each endpoint is supplied in Bitvavo API documentation.
            # This call returns the amount of points left. If you make more requests than permitted by the weight limit,
            # your IP or API key is banned.
            limit = self.bitvavo_engine.getRemainingLimit()
            try:
                while (limit > 0):
                    time.sleep(0.5)
                    limit = self.bitvavo_engine.getRemainingLimit()
            except KeyboardInterrupt:
                self.bitvavo_socket.closeSocket()


    # Shall I re-explain main? Naaaaaaaaaa.
    if __name__ == '__main__':
        bvavo = BitvavoImplementation()
        bvavo.a_trading_strategy()
        bvavo.wait_and_close()
    ```
   
1. **Add security information**

    You must supply your security information to trade on Bitvavo and see your account information using the authenticate methods. 
    Replace the values of  `api_key` and `api_secret` with your credentials from [Bitvavo Dashboard](https://account.bitvavo.com/user/api). 

    You can retrieve public information such as available markets, assets and current market without supplying your key and secret. 
    However, unauthenticated calls have lower rate limits based on your IP address, and your account is blocked for longer if 
    you exceed your limit.

1. **Run your app**

    - Command line warriors: `python3 <filename>`.
    - IDE heroes: press the big green button.
 
Your app connects to Bitvavo and returns a list the latest trade price for each market. 
You use this data to implement your trading logic.


## About the SDK

This section explains global concepts about Bitvavo SDK for Python. 

### Rate limit

Bitvavo uses a weight based rate limiting system. 
Your app is limited to 1000 weight points per IP or API key per minute. 
When you make a call to Bitvavo API, your remaining weight points are returned in the header of each REST request. 

Websocket methods do not return your returning weight points, you track your remaining weight points with a call to:
```
limit = bitvavo.getRemainingLimit()
```


If you make more requests than permitted by the weight limit, your IP or API key is banned. 

The rate weighting for each endpoint is supplied in the [Bitvavo API documentation](https://docs.bitvavo.com/).

### Requests

For all methods, required parameters are passed as separate values, optional parameters are passed as a dictionary. 
Return parameters are in dictionary format: `response['<key>'] = '<value>'`. However, as a limit order requires 
more information than a market order, some optional parameters are required when you place an order.

### Security

You must set your API key and secret for authenticated endpoints, public endpoints do not require authentication. 
