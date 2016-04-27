#!/usr/bin/env python2

from wlox_api import *

isx = WLOXAPI('API-key', 'API-secret')

# Public calls on ISX API tests.
data = isx.stats()
print("API call stats:")
print(data)
print("\n")

data = isx.historical_prices()
print("API call historical-prices:")
print(data)
print("\n")

data = isx.order_book()
print("API call order-book:")
print(data)
print("\n")

data = isx.transactions()
print("API call transactions:")
print(data)
print("\n")

# Private calls on ISX API tests.

data = isx.balances_and_info()
print("Private API call balances-and-info:")
print(data)
print("\n")

data = isx.openorders()
print("Private API call open-orders:")
print(data)
print("\n")

data = isx.user_transactions()
print("Private API call user-transactions:")
print(data)
print("\n")
