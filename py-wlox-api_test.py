#!/usr/bin/env python2

#  Tests for the py-wlox-api library.
#  Copyright (C) 2016  Myckel Habets

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

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

data = isx.crypto_deposit_address_get()
print("Private API call crypto-deposit-address/get:")
print(data)
print("\n")

data = isx.crypto_deposit_address_new()
print("Private API call crypto-deposit-address/new:")
print(data)
print("\n")

data = isx.deposits_get()
print("Private API call deposits/get:")
print(data)
print("\n")



