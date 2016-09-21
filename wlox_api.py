#  Python library to access WLOX-based cryptocurrency exchanges.
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

import urllib2
import urllib
import base64
import time
import hashlib
import hmac
import json

class WLOXAPI:
   def __init__(self, api_key, api_secret, api_uri='https://isx.is/api/'):
      self.api_key = api_key
      self.api_secret = api_secret
      self.api_uri = api_uri

   def query(self, method, params={}, private=True):
      # Headers
      headers = {'User-Agent': "Py-WLOX-API", 'Content-Type': 'application/json;charset=utf-8'}

      if private:
         nonce = str(int(time.time() * 1000))

         # Construct the params JSON string.
         # First obtain the params keys
         params_idx = []
         for key in params.keys():
            params_idx.append(key)
 
         # Construct the string
         data_str = '"nonce":'+nonce+',"api_key":"'+self.api_key+'"'
         for key in params_idx:
            if key is 'limit':
               # limit is a numerical value, don't quote it.
               data_str = data_str + ',"' + str(key) + '":' + str(params[key])
            else:
               data_str = data_str + ',"' + str(key) + '":"' + str(params[key]) + '"'

         json_str  = '{' + data_str + '}'
         json_str = json_str.encode("utf-8")
         json_base64 = base64.b64encode(json_str)

         # create the signature
         signature = hmac.new(self.api_secret, json_base64, digestmod=hashlib.sha256).hexdigest()

         # add signature to request parameters
         data_str = data_str + ',"signature":"' + signature + '"'
         json_str  = '{' + data_str + '}'
         json_str = json_str.encode("utf-8")

         # params are passed as POST vars to the server
         method_uri = self.api_uri + method
      else:
         # params are passed as GET vars to the server
         params = urllib.urlencode(params)
         method_uri = self.api_uri +  method + '?' + params

      if private:
         req = urllib2.Request(method_uri, json_str, headers=headers)
      else:
         req = urllib2.Request(method_uri, headers=headers)
      self.res = urllib2.urlopen(req)
      result = self.decode_json(self.res)
      return(result)

   def stats(self, market='aur', currency='isk'):
      method = 'stats'
      params =  {'market': market, 'currency' : currency}
      result = self.query(method, params, private=False)
      return(result)

   def historical_prices(self, market='aur', currency='isk', timeframe='1mon'):
      # timeframe (string) - The timeframe for your request. Permitted values are "1mon", "3mon", "6mon", "1year" 
      # and "ytd". Default is "1mon".
      method = 'historical-prices'
      params = {'market': market, 'currency': currency, 'timeframe': timeframe}
      result = self.query(method, params, private=False)
      return(result)

   def order_book(self, market='aur', currency='isk'):
      method = 'order-book'
      params = {'market': market, 'currency': currency}
      result = self.query(method, params, private=False)
      return(result)

   def transactions(self, market='aur', currency='isk', limit=10):
      method = 'transactions'
      params = {'market': market, 'currency': currency, 'limit': limit}
      result = self.query(method, params, private=False)
      data = result['transactions']
      return(data)

   def balances_and_info(self):
      method = 'balances-and-info'
      result = self.query(method, private=True)
      return(result)

   def openorders(self, market='aur', currency='isk'):
      method = 'open-orders'
      params = {'market': market, 'currency': currency}
      result = self.query(method, params, private=True)
      return(result)

   def user_transactions(self, market='aur', currency='isk', limit=10, side='buy'):
      method = 'user-transactions'
      params = {'market': market, 'currency': currency, 'limit': limit, 'side': side}
      result = self.query(method, params, private=True)
      return(result)

   def crypto_deposit_address_get(self, market='aur', limit=1):
      method = 'crypto-deposit-address/get'
      params = {'market': market, 'limit': limit}
      result = self.query(method, params, private=True)
      return(result)

   def crypto_deposit_address_new(self, market='aur'):
      method = 'crypto-deposit-address/new'
      params = {'market': market}
      result = self.query(method, params, private=True)
      return(result)

   def deposits_get(self, currency='aur', limit=1, status='completed'):
      method = 'deposits/get'
      params = {'currency': currency, 'limit': limit, 'status': status}
      result = self.query(method, params, private=True)
      return(result)

   def withdrawals_get(self, currency='aur', limit=1, status='completed'):
      method = 'withdrawals/get'
      params = {'currency': currency, 'limit': limit, 'status': status}
      result = self.query(method, params, private=True)
      return(result)

   def withdrawals_new(self, amount='0.00', address):
      # TODO: add fiat withdrawals
      method = 'withdrawals/new'
      currency = 'aur'
      params = {'currency': currency, 'amount': amount, 'address': address}
      result = self.query(method, params, private=True)
      return(result)

   def orders_new(self, market='aur', currency='isk', side, ordertype='limit', limit_price='0.00', stop_price='0.00', amount='0.00'):
      method = 'orders/new'
      params = {'market': market, 'currency': currency, 'side': side, 'type': ordertype, 'limit_price': limit_price, 'stop_price': stop_price, 'amount': amount}
      result = self.query(method, params, private=True)
      return(result)

   def orders_edit(self, orderid, ordertype, limit_price, stop_price, amount):
      method = 'orders/edit'
      params = {'id': orderid, 'type': ordertype, 'limit_price': limit_price, 'stop_price': stop_price, 'amount': amount}
      result = self.query(method, params, private=True)
      return(result)

   def orders_cancel(self, orderid):
      method = 'orders/cancel'
      if orderid is 'all':
         params = {'all': '1'}
      else:
         params = {'id': orderid}
      result = self.query(method, params, private=True)
      return(result)

   def orders_status(self, orderid):
      method = 'orders/status'
      params = {'id': orderid}
      result = self.query(method, params, private=True)
      return(result)

   def decode_json(self, json_str):
      try:
         result = json.load(json_str)
      except:
         result = False
      return(result)