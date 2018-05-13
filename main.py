import webapp2

from app.handlers import base, bot

app = webapp2.WSGIApplication([
    ('/', base.MainPage),
    ('/about', base.AboutPage),
    ('/set_webhook', bot.SetWebhookHandler),
    ('/get_webhook', bot.GetWebhookHandler),
    ('/webhook', bot.WebhookHandler),
], debug=True)
