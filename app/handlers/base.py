import webapp2
import jinja2
import os

from google.appengine.api import users

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

    @__admin_required
    def get(self):
        kwargs = {
            'title': 'Settings',
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
