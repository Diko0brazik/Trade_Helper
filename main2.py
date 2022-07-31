import os
from struct import pack
import sys
from bfxapi import Client, Order
import asyncio
import configparser

class test():
    def __init__(self):
        pass

    async def get_seeds(self, bfx):
        self.candles = await bfx.rest.get_seed_candles('tBTCUSD')

    async def get_active_position(self, bfx):
        self.active_positions = await bfx.rest.get_active_position()

    async def get_active_orders(self, bfx):
        self.active_orders = await bfx.rest.get_active_orders('')
        



def main():
    apikey, apisecret = loadconfig()
    bfx = Client(
        API_KEY=apikey,
        API_SECRET=apisecret
        )
    t= test()

    async def get_seeds():
        candles = await bfx.rest.get_seed_candles('tBTCUSD')
        print (candles)

    #asyncio.get_event_loop().run_until_complete(t.get_seeds(bfx))
    asyncio.get_event_loop().run_until_complete(t.get_active_position(bfx))
    asyncio.get_event_loop().run_until_complete(t.get_active_orders(bfx))
    print(t.active_orders)

    pass

def loadconfig():
    config = configparser.ConfigParser() #.read('config.ini')
    config.read('config.ini')
    apikey = config['default']['apikey']
    apisecret = config['default']['apisecret']
    return apikey, apisecret

if __name__ == '__main__':
    main()