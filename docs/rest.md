
# Bitvavo SDK for Python, REST implementation

Crypto starts with Bitvavo. 
You use Bitvavo SDK for Python to buy, sell, and store over 200 digital assets on Bitvavo from inside your app. 

To trade and execute your advanced trading strategies, Bitvavo SDK for Python is a wrapper that enables you to easily call every endpoint in [Bitvavo API](https://docs.bitvavo.com/).

- [Prerequisites](#prerequisites) - what you need to start developing with Bitvavo SDK for Python
- [API reference](https://docs.bitvavo.com/) - information on the specifics of every parameter

This page gives reference information for REST calls made using Bitvavo SDK for Python.

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

## About the SDK

This section explains global concepts about Bitvavo SDK for Python. 

### Rate limit

Bitvavo uses a weight based rate limiting system. 
Your app is limited to 1000 weight points per IP or API key per minute. 
When you make a call to Bitvavo API, your remaining weight points are returned in the header of each REST request.
If you make more requests than permitted by the weight limit, your IP or API key is banned.
The rate weighting for each endpoint is supplied in the [Bitvavo API documentation](https://docs.bitvavo.com/).

### Requests

For all methods, required parameters are passed as separate values, optional parameters are passed as a dictionary. 
Return parameters are in dictionary format: `response['<key>'] = '<value>'`. However, as a limit order requires 
more information than a market order, some optional parameters are required when you place an order.

### Security

You must set your API key and secret for authenticated endpoints, public endpoints do not require authentication. 
