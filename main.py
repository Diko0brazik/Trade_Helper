import configparser
import asyncio
import aiohttp
import time
import json
import datetime

'''
order
position
open orders
filled orders

show 
position, stop in usd, profit in usd

'''

def main():
    bitfinex_load_position()

    for position in positions:
        pass
        #make a row in a table
 
def main_window():
    pass

def bitfinex_load_position():
    apikey, apisecret = loadconfig()
    client = BfxRest(apikey, apisecret)
    wallets = client.get_wallets()
    print(wallets)

class BfxRest:
    """
    BFX rest interface contains functions which are used to interact with both the public
    and private Bitfinex http api's.
    To use the private api you have to set the API_KEY and API_SECRET variables to your
    api key.
    """
    def __init__(self, API_KEY, API_SECRET, host='https://api.bitfinex.com/v2', loop=None,
                 logLevel='INFO', parse_float=float, *args, **kwargs):
        self.loop = loop or asyncio.get_event_loop()
        self.API_KEY = API_KEY
        self.API_SECRET = API_SECRET
        self.host = host
        # this value can also be set to bfxapi.decimal for much higher precision
        self.parse_float = parse_float
        #self.logger = CustomLogger('BfxRest', logLevel=logLevel)

    def post(self, endpoint, data={}, params=""):
        """
        Send a pre-signed POST request to the bitfinex api
        @return response
        """
        host = self.host
        url = '{}/{}'.format(host, endpoint)
        sData = json.dumps(data)
        headers = generate_auth_headers(
            self.API_KEY, self.API_SECRET, endpoint, sData)
        headers["content-type"] = "application/json"
        with aiohttp.ClientSession() as session:
            with session.post(url + params, headers=headers, data=sData) as resp:
                text =  resp.text()
                if resp.status < 200 or resp.status > 299:
                    raise Exception('POST {} failed with status {} - {}'
                                    .format(url, resp.status, text))
                parsed = json.loads(text, parse_float=self.parse_float)
                return parsed


    def get_wallets(self):
        """
        Get all wallets on account associated with API_KEY - Requires authentication.
        @return Array <models.Wallet>
        """
        endpoint = "auth/r/wallets"
        raw_wallets =  self.post(endpoint)
        #return [Wallet(*rw[:5]) for rw in raw_wallets]
        return raw_wallets


def loadconfig():
    config = configparser.ConfigParser() #.read('config.ini')
    config.read('config.ini')
    apikey = config['default']['apikey']
    apisecret = config['default']['apisecret']
    return apikey, apisecret








import hashlib
import hmac
import time

def generate_auth_headers(API_KEY, API_SECRET, path, body):
  """
  Generate headers for a signed payload
  """
  nonce = str(_gen_nonce())
  signature = "/api/v2/{}{}{}".format(path, nonce, body)
  h = hmac.new(API_SECRET.encode('utf8'), signature.encode('utf8'), hashlib.sha384)
  signature = h.hexdigest()

  return {
    "bfx-nonce": nonce,
    "bfx-apikey": API_KEY,
    "bfx-signature": signature
  }

def _gen_signature(API_KEY, API_SECRET, nonce):
  authMsg = 'AUTH{}'.format(nonce)
  secret = API_SECRET.encode('utf8')
  sig = hmac.new(secret, authMsg.encode('utf8'), hashlib.sha384).hexdigest()

  return authMsg, sig

def _gen_nonce():
  return int(round(time.time() * 1000000))

def gen_unique_cid():
  return int(round(time.time() * 1000))


if __name__ == '__main__':
    main()