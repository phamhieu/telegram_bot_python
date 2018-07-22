import json
import unittest
import urllib

from google.appengine.ext import ndb
from google.appengine.ext import testbed

import app.models.chat as chat_model


class TestHandlers(unittest.TestCase):
    def setUp(self):
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Initialize urlfetch
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def tearDown(self):
        self.testbed.deactivate()

    def test_get_text_reply(self):
        body_str = (
            '{\"message\": {\"date\": 1523750946, '
            '\"text\": \"i love you\", \"from\": {\"username\": '
            '\"heosua\", \"first_name\": \"Hieu\", \"last_name\": '
            '\"Pham Trung\", \"is_bot\": false, \"language_code\": '
            '\"en-US\", \"id\": 222222222 }, \"message_id\": 122, '
            '\"chat\": {\"username\": \"heosua\", \"first_name\": '
            '\"Hieu\", \"last_name\": \"Pham Trung\", \"type\": '
            '\"private\", \"id\": 222222222 } }, \"update_id\": 444444444 }'
        )
        body = json.loads(body_str)
        chat = chat_model.Handler(body)
        method, data = chat.get_reply()
        self.assertEqual(method, 'sendMessage')
        text = 'Yo Hieu I got your message'
        result = urllib.urlencode({
            'text': text.encode('utf-8'),
            'chat_id': '222222222',
            'reply_to_message_id': '122'
        })
        self.assertEqual(data, result)

    def test_get_command_reply(self):
        body_str = (
            '{\"message\": {\"from\": {\"username\": \"heosua\", '
            '\"first_name\": \"Hieu\", \"last_name\": \"Pham Trung\", '
            '\"is_bot\": false, \"language_code\": \"en-US\", '
            '\"id\": 333333333 }, \"text\": \"/sayhello@HeosuaBot\", '
            '\"entities\": [{\"length\": 19, \"type\": \"bot_command\", '
            '\"offset\": 0 } ], \"chat\": {\"type\": \"supergroup\", '
            '\"id\": 333333333, \"title\": \"Bot test\"}, '
            '\"date\": 1523750512, \"message_id\": 92 }, '
            '\"update_id\": 516632302 }'
        )
        body = json.loads(body_str)
        chat = chat_model.Handler(body)
        method, data = chat.get_reply()
        self.assertEqual(method, 'sendMessage')
        text = 'Hi, nice to meet you'
        result = urllib.urlencode({
            'text': text.encode('utf-8'),
            'chat_id': '333333333',
            'reply_to_message_id': '92'
        })
        self.assertEqual(data, result)
