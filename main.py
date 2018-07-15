import webapp2

from app.handlers import base, bot, settings

app = webapp2.WSGIApplication([
    webapp2.Route('/login', base.LoginHandler, name='login'),
    webapp2.Route('/logout', base.LogoutHandler, name='logout'),
    webapp2.Route('/403', base.Page403, name='403'),
    ('/', base.MainPage),
    ('/about', base.AboutPage),
    webapp2.Route('/settings', settings.SettingsHandler, name='settings'),
    webapp2.Route
    (
        '/settings/config',
        settings.ConfigHandler,
        name='settings_config'
    ),
    webapp2.Route
    (
        '/settings/webhook',
        settings.WebhookHandler,
        name='settings_webhook'
    ),
    ('/webhook', bot.WebhookHandler),
], debug=True)
