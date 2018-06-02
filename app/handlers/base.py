import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               extensions=['jinja2.ext.autoescape'],
                               autoescape=False,
                               trim_blocks=True)


class Handler(webapp2.RequestHandler):
    def render_template(self, template_name, **kwargs):
            if not kwargs:
                kwargs = {}
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
