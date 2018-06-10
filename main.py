import webapp2

from app.handlers import base, bot

app = webapp2.WSGIApplication([
    webapp2.Route('/login', base.LoginHandler, name='login'),
    webapp2.Route('/logout', base.LogoutHandler, name='logout'),
    webapp2.Route('/403', base.Page403, name='403'),
    ('/', base.MainPage),
    ('/about', base.AboutPage),
    ('/settings', base.SettingsPage),
    ('/set_webhook', bot.SetWebhookHandler),
    ('/get_webhook', bot.GetWebhookHandler),
    ('/webhook', bot.WebhookHandler),
], debug=True)
