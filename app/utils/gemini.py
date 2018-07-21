import json
import logging
from decimal import Decimal

from google.appengine.api import urlfetch

__URL_PRODUCTION = 'https://api.gemini.com/v1'


def get_btc_price():
    url = __URL_PRODUCTION + "/pubticker/btcusd"
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            jsonstr = result.content
            jsonobj = json.loads(jsonstr)
            return jsonobj['last'] if jsonobj else None
        else:
            logging.exception(
                'get_btc_price failed {}'.format(result.status_code)
                )
            return None
    except:
        logging.exception('get_btc_price exception fetching url')
        return None


def get_btc_booking():
    url = __URL_PRODUCTION + "/book/btcusd"
    try:
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            jsonstr = result.content
            jsonobj = json.loads(jsonstr)
            bids = jsonobj['bids']
            max_bid = 0
            for bid in bids:
                price = Decimal(bid['price'])
                max_bid = price if price > max_bid else max_bid
            asks = jsonobj['asks']
            min_ask = 999999999
            for ask in asks:
                price = Decimal(ask['price'])
                min_ask = price if price < min_ask else min_ask
            return max_bid, min_ask
        else:
            logging.exception(
                'get_btc_booking failed {}'.format(result.status_code)
                )
            return None, None
    except:
        logging.exception('get_btc_booking exception fetching url')
        return None, None
