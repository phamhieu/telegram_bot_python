import webapp2
import json
import logging

from google.appengine.api import urlfetch

import app.models.chat as chat


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
