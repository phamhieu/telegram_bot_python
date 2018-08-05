import logging
import urllib
import urllib2

from app.models.config import TelegramConfig
from app.utils import gemini


class Handler(object):
    def __init__(self, body):
        self.body = body
        self.message = self.__get_message()
        self.telegramBaseUrl = TelegramConfig.get_base_url()

    def __get_message(self):
        if self.body:
            if 'message' in self.body:
                message = self.body['message']
            elif 'edited_message' in self.body:
                message = self.body['edited_message']
            return message
        return None

    def __encode_reply_decorator(func):
        def func_wrapper(self, **kwargs):
            method, message_dict = func(self, **kwargs)
            return method, urllib.urlencode(message_dict)
        return func_wrapper

    def __get_reply_decorator(func):
        def func_wrapper(self):
            method, reply_dict = func(self)
            reply_dict['chat_id'] = str(self.message['chat']['id'])
            reply_dict['reply_to_message_id'] = str(self.message['message_id'])
            return method, reply_dict
        return func_wrapper

    @__encode_reply_decorator
    @__get_reply_decorator
    def __get_default_reply(self):
        msg = 'I understand only text and sticker messages'
        data = {
            'text': msg.encode('utf-8')
        }
        return 'sendMessage', data

    @__encode_reply_decorator
    @__get_reply_decorator
    def __get_text_reply(self):
        first_name = self.message['from']['first_name']
        msg = 'Yo {} I got your message'.format(first_name)
        data = {
            'text': msg.encode('utf-8')
        }
        return 'sendMessage', data

    @__encode_reply_decorator
    @__get_reply_decorator
    def __get_sticker_reply(self):
        file_id = self.message['sticker']['file_id']
        data = {
            'sticker': file_id.encode('utf-8'),
        }
        return 'sendSticker', data

    @__encode_reply_decorator
    @__get_reply_decorator
    def __get_command_reply(self):
        commant_text = self.message['text']
        if '/checkbcprice' in commant_text:
            last_price = gemini.get_btc_price()
            if last_price is not None:
                msg = '1 btcUSD = $' + last_price
            else:
                msg = 'Failed to retrieve price data.'
            reply_dict = {'text': msg.encode('utf-8')}
        elif '/checkbcbooking' in commant_text:
            max_bid, min_ask = gemini.get_btc_booking()
            if max_bid is not None and min_ask is not None:
                msg = 'maxBid= $' + str(max_bid) + '  |  minAsk=$' + str(min_ask)
            else:
                msg = 'Failed to retrieve booking data.'
            reply_dict = {'text': msg.encode('utf-8')}
        elif '/sayhello' in commant_text:
            msg = 'Hi, nice to meet you'
            reply_dict = {
                'text': msg.encode('utf-8')
            }
        else:
            msg = 'I know this command. Let me think...'
            reply_dict = {'text': msg.encode('utf-8')}
        return 'sendMessage', reply_dict

    def get_reply(self):
        if self.message:
            if 'entities' in self.message:
                for entity in self.message['entities']:
                    if entity['type'] == 'bot_command':
                        return self.__get_command_reply()
            # if not command reply, check for other replies
            if 'sticker' in self.message:
                return self.__get_sticker_reply()
            elif 'text' in self.message:
                return self.__get_text_reply()
            else:
                return self.__get_default_reply()
        return None, None

    def send_reply(self):
        reply_method, data = self.get_reply()
        if data:
            requestUrl = '{}/{}'.format(self.telegramBaseUrl, reply_method)
            resp = urllib2.urlopen(requestUrl, data).read()
            logging.info('Reply is sent with response: {0}'.format(resp))
        else:
            logging.info('Send reply fail')
            resp = None
