import webapp2
import jinja2
import json
import os

from google.appengine.api import users
from google.appengine.api import urlfetch

from app.models.config import TelegramConfig

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False,
                               trim_blocks=True)


class Handler(webapp2.RequestHandler):
    def render_template(self, template_name, **kwargs):
        if not kwargs:
            kwargs = {}
        user = users.get_current_user()
        if user:
            kwargs['user'] = user
        t = jinja_env.get_template(template_name)
        self.response.write(t.render(kwargs))


class MainPage(Handler):
    def get(self):
        kwargs = {
            'title': 'Home',
        }
        self.render_template('home.html', **kwargs)


class AboutPage(Handler):
    def get(self):
        kwargs = {
            'title': 'About',
        }
        self.render_template('about.html', **kwargs)


class SettingsPage(Handler):
    def __init__(self, *args, **kwargs):
        super(SettingsPage, self).__init__(*args, **kwargs)
        self.telegramBaseUrl = TelegramConfig().get_base_url()

    def __admin_required(func):
        def func_wrapper(self, *args, **kwargs):
            user = users.get_current_user()
            if user:
                email = user.email()
                admins = [
                    "admin1@gmail.com",
                    "admin2@gmail.com"
                ]
                if email in admins:
                    return func(self, *args, **kwargs)
                else:
                    return webapp2.redirect_to("403")
            else:
                return webapp2.redirect_to("login")
        return func_wrapper

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

    @__admin_required
    def get(self):
        kwargs = {
            'title': 'Settings',
        }
        kwargs['webhook_url_value'] = self.__get_webhook_url()
        self.render_template('settings.html', **kwargs)

    @__admin_required
    def post(self):
        kwargs = {
            'page_name': 'Webhooks'
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
        self.render_template('settings.html', **kwargs)


class LoginHandler(Handler):
    def get(self):
        self.redirect(users.create_login_url('/'))


class LogoutHandler(Handler):
    def get(self):
        self.redirect(users.create_logout_url('/'))


class Page403(Handler):
    def get(self):
        kwargs = {
            'title': '403 Forbidden',
        }
        self.render_template('403.html', **kwargs)
