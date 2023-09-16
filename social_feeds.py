import datetime as dt
import time
import logging

from optibook.synchronous_client import Exchange
from optibook.common_types import SocialMediaFeed

logging.getLogger('client').setLevel('ERROR')    

from testing_news import get_mood_for_news, get_relevat_instrument_from_news

def get_social_feed(exchange):
    social_feeds = exchange.poll_new_social_media_feeds()
    result = {}
    
    if social_feeds:
        for feed in social_feeds:
            instruments = get_relevat_instrument_from_news(feed.post)
            if instruments:
                mood = get_mood_for_news(feed.post)
                for instrument in instruments:
                    if instrument:
                        result[instrument] = mood
                
            print(f'{feed.timestamp}: {feed.post}')
    
    return result
    