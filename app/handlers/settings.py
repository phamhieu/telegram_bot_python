import webapp2
import json

from google.appengine.api import urlfetch

from app.models.config import TelegramConfig
import app.handlers.base as base


class SettingsHandler(base.Handler):
    @base.admin_required
    def get(self):
        return webapp2.redirect_to("settings_config")


class ConfigHandler(base.Handler):
    @base.admin_required
    def get(self):
        kwargs = {
            'page_name': 'Config'
        }
        kwargs['telegram_bot_token_value'] = TelegramConfig.get_telgram_token()
        self.render_template('settings.config.html', **kwargs)

    @base.admin_required
    def post(self):
        kwargs = {
            'page_name': 'Config'
        }
        new_botToken = self.request.get('telegram_bot_token')
        TelegramConfig.set_telegram_token(new_botToken)
        kwargs['message'] = {
            'category': 'success',
            'title': 'Success!',
            'text': 'Update Successfully'
        }
        kwargs['telegram_bot_token_value'] = new_botToken
        self.render_template('settings.config.html', **kwargs)


class WebhookHandler(base.Handler):
    def __init__(self, *args, **kwargs):
        super(WebhookHandler, self).__init__(*args, **kwargs)
        self.telegramBaseUrl = TelegramConfig.get_base_url()

    def __get_webhook_url(self):
        url = '{0}/getWebhookInfo'.format(self.telegramBaseUrl)
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                jsonstr = result.content
                jsonobj = json.loads(jsonstr)
                return jsonobj['result']['url']
            else:
                return None
        except:
            return None

    def __set_webhook_url(self, new_url):
        url = '{0}/setWebhook?url={1}'.format(self.telegramBaseUrl, new_url)
        try:
            result = urlfetch.fetch(url)
            if result.status_code == 200:
                jsonstr = result.content
                jsonobj = json.loads(jsonstr)
                message = jsonobj['description']
                if 'error_code' in jsonobj:
                    success = False
                    error_code = jsonobj['error_code']
                    message = 'Code({0}) {1}'.format(error_code, message)
                else:
                    success = True
                return success, message
            else:
                return False, None
        except:
            return False, None

    @base.admin_required
    def get(self):
        kwargs = {
            'page_name': 'Webhook'
        }
        kwargs['webhook_url_value'] = self.__get_webhook_url()
        self.render_template('settings.webhook.html', **kwargs)

    @base.admin_required
    def post(self):
        kwargs = {
            'page_name': 'Webhook'
        }
        new_url = self.request.get('webhook_url')
        success, message = self.__set_webhook_url(new_url)
        if success:
            kwargs['message'] = {
                'category': 'success',
                'title': 'Success!',
                'text': message
            }
            kwargs['webhook_url_value'] = new_url
        else:
            kwargs['message'] = {
                'category': 'danger',
                'title': 'Error!',
                'text': message
            }
        self.render_template('settings.webhook.html', **kwargs)
