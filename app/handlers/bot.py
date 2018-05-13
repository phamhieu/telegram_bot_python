import webapp2
import urllib
import urllib2
import json
import logging

from google.appengine.api import urlfetch

import app.models.chat as chat

TOKEN = 'xxxxxx:YOUR_TELEGRAM_BOT_TOKEN'
BASE_URL = 'https://api.telegram.org/bot' + TOKEN


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            requestUrl = '{}/{}'.format(BASE_URL, 'setWebhook')
            requestParam = urllib.urlencode({'url': url})
            response = urllib2.urlopen(requestUrl, requestParam)
            self.response.write(json.dumps(json.load(response)))
        else:
            self.response.write('Invalid webhook URL: {}<br>'.format(url))


class GetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        requestUrl = '{}/{}'.format(BASE_URL, 'getWebhookInfo')
        response = urllib2.urlopen(requestUrl)
        self.response.write(json.dumps(json.load(response)))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        if body:
            logging.info('Update body: {}'.format(body))
            chat_handler = chat.Handler(body)
            chat_handler.send_reply()
        else:
            logging.info('Telegram update body is Invalid')
