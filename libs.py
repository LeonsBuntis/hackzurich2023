from math import floor, ceil
import time

def print_positions_and_pnl(exchange):
    positions = exchange.get_positions()
    pnl = exchange.get_pnl()

    print('Positions:')
    for instrument_id in positions:
        print(f'  {instrument_id:10s}: {positions[instrument_id]:4.0f}')

    print(f'\nPnL: {pnl:.2f}')

    
def round_down_to_tick(price, tick_size):
    """
    Rounds a price down to the nearest tick, e.g. if the tick size is 0.10, a price of 0.97 will get rounded to 0.90.
    """
    return floor(price / tick_size) * tick_size


def round_up_to_tick(price, tick_size):
    """
    Rounds a price up to the nearest tick, e.g. if the tick size is 0.10, a price of 1.34 will get rounded to 1.40.
    """
    return ceil(price / tick_size) * tick_size    
    
def insert_quotes(exchange, instrument, bid_price, ask_price, bid_volume, ask_volume):
    if bid_volume > 0:
        # Insert new bid limit order on the market
        exchange.insert_order(
            instrument_id=instrument.instrument_id,
            price=bid_price,
            volume=bid_volume,
            side='bid',
            order_type='limit',
        )
        
        # Wait for some time to avoid breaching the exchange frequency limit
        time.sleep(0.05)

    if ask_volume > 0:
        # Insert new ask limit order on the market
        exchange.insert_order(
            instrument_id=instrument.instrument_id,
            price=ask_price,
            volume=ask_volume,
            side='ask',
            order_type='limit',
        )

        # Wait for some time to avoid breaching the exchange frequency limit
        time.sleep(0.05)