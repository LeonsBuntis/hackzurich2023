from optibook.synchronous_client import Exchange
# from basic_trader import start_trading
from smarter_trader import start_trading
from IPython.display import clear_output
from social_feeds import get_social_feed
# from testing_feeds import get_mood_for_news

import asyncio
import time
import logging
logger = logging.getLogger('client')
logger.setLevel('ERROR')

print("Setup was successful.")

exchange = Exchange()
exchange.connect()

INSTRUMENTS = exchange.get_instruments()

QUOTED_VOLUME = 10
FIXED_MINIMUM_CREDIT = 0.15
PRICE_RETREAT_PER_LOT = 0.005
POSITION_LIMIT = 100

hold = {
    'CSCO': {'value': 0, 'mood': None},
    'PFE': {'value': 0, 'mood': None},
    'SAN': {'value': 0, 'mood': None},
    'ING': {'value': 0, 'mood': None},
    'NVDA': {'value': 0, 'mood': None},
}

async def trader():
    global hold
    while True:
        start_trading(exchange, INSTRUMENTS, QUOTED_VOLUME, FIXED_MINIMUM_CREDIT, PRICE_RETREAT_PER_LOT, POSITION_LIMIT, hold)
        
        await asyncio.sleep(2)
        
        for k, v in hold.items():
            if v['value'] > 0:
                hold[k]['value'] = v['value'] - 1
        
        # Clear the displayed information after waiting
        clear_output(wait=True)
        
async def newsChecker():
    global hold
    while True:
        social_feeds = get_social_feed(exchange)
    
        if social_feeds:
            for feed, mood in social_feeds.items():
                if not feed:
                    continue
                
                if mood < 0.45:
                    hold[feed] = {'value': 12, 'mood': 'ask'}
                    exchange.delete_orders(feed)
                    print(f'Someting bad happened to {feed}')
                
                elif mood > 0.55:
                    hold[feed] = {'value': 12, 'mood': 'bid'}
                    exchange.delete_orders(feed)
                    print(f'Someting good happened to {feed}')
                else:
                    exchange.delete_orders(feed)
                    continue
        else:
            print(f'\n --- No news --- \n')
            
        await asyncio.sleep(5)
        
        
loop = asyncio.get_event_loop()
task1 = asyncio.ensure_future(trader())
task2 = asyncio.ensure_future(newsChecker())

loop.run_until_complete(asyncio.gather(task1, task2))