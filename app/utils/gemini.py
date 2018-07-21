import json
import logging

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
