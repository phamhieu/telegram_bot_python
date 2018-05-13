import json
import unittest
import urllib

import app.models.chat as chat_model


class TestHandlers(unittest.TestCase):
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
