import urllib2
import urllib
import time
import hashlib
import hmac
import json

class WLOXAPI:
   def __init__(self, api_key, api_secret, api_uri='https://beta.isx.is/api/'):
      self.api_key = api_key
      self.api_secret = api_secret
      self.api_uri = api_uri

   def query(self, method, params={}, private=True):
      # Headers
      headers = {'User-Agent': "Py-WLOX-API"}

      if private:
         params['api_key'] = self.api_key
         params['nonce'] = time.time()

         # create the signature
         message = bytes(json.dumps(params)).encode('utf-8')
         secret = bytes(self.api_secret).encode('utf-8')
         signature = hmac.new(secret, message, digestmod=hashlib.sha256).hexdigest()

         # add signature to request parameters
         params['signature'] = signature

         # params are passed as POST vars to the server
         params = urllib.urlencode(params)
         method_uri = self.api_uri + method
      else:
         # params are passed as GET vars to the server
         params = urllib.urlencode(params)
         method_uri = self.api_uri +  method + '?' + params

      if private:
         req = urllib2.Request(method_uri, params, headers=headers)
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

   def decode_json(self, json_str):
      try:
         result = json.load(json_str)
      except:
         result = False
      return(result)