import logging

from google.appengine.ext import ndb
from google.appengine.ext.ndb import model


class Config(ndb.Model):
    value = ndb.StringProperty()

    @classmethod
    def set(self, name, inputValue):
        entity = self(key=model.Key(self, name))
        entity.populate(value=inputValue)
        entity.put()

    @classmethod
    def get(self, name):
        NOT_SET_VALUE = u'!!!__ NOT SET __!!!'

        entity = self(key=model.Key(self, name))
        entity.populate(value=NOT_SET_VALUE)
        txn = lambda: entity.put() if not entity.key.get() else entity.key
        retval = model.transaction(txn).get()

        if retval.value == NOT_SET_VALUE:
            logging.error((
                '%s %s not found in the database. A placeholder ' +
                'record has been created. Go to the Developers Console '
                'for your app in App Engine, look up the Settings record '
                'with name=%s and enter its value in that record\'s value '
                'field.'
                ) % (
                self.__name__,
                name,
                name)
                )

        return retval.value


TELEGRAM_BOT_TOKEN_KEY = "TELEGRAM_BOT_TOKEN_KEY"


class TelegramConfig(Config):
    @classmethod
    def get_telgram_token(self):
        return self.get(TELEGRAM_BOT_TOKEN_KEY)

    @classmethod
    def set_telegram_token(self, inputValue):
        self.set(TELEGRAM_BOT_TOKEN_KEY, inputValue)

    @classmethod
    def get_base_url(self):
        token = self.get(TELEGRAM_BOT_TOKEN_KEY)
        return 'https://api.telegram.org/bot{}'.format(token)
