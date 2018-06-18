# telegram_bot_python

Telegram bot source code in Python. You can read more tutorials at [CodeMyBot.com](http://codemybot.com)

## CHANGELOG

## 0.1.0 - 2018-06-17
### Changed
- Update `base.py`, `base.html` with login/logout menu item.

## 0.0.9 - 2018-06-10
### Added
- Add `templates/settings.html`
- Add `templates/403.html`
- Support `login`/`logout` with Google Sign-In

### Changed
- Update `main.py` and `base.py`

## 0.0.8 - 2018-06-01
### Added
- Add `templates/about.html`
- Add `templates/home.html`

### Changed
- Update `base.html` and `base.py` to support 2 new pages

## 0.0.7 - 2018-05-27
### Added
- Add `static/css/style.css`

### Changed
- Update `base.html` to use Bootstrap 4

## 0.0.6 - 2018-05-20
### Added
- Add `templates/base.html`

### Changed
- Refactor `base.py` to use jinja2 for rendering

## 0.0.5 - 2018-05-13
### Added
- Add `runner.py`, `handler_bot_test.py` for basic unittest

### Changed
- Update `chat.py` to support decorator methods
- Clean repo history

## 0.0.4 - 2018-04-27
### Added
- Add `chat.py` under `models` package to handle message replying
- Update `bot.py` to use `chat.py`

### Changed
- Refactor `main.py` into sub modules
- Use str.format() 

## 0.0.2 - 2018-04-15
### Added
- defaultReply method to support all kind of messages
- Add 'reply_to_message_id' to reply payload. Easier for us to know what message the bot is replying to. 

### Removed
- Remove 'disable_web_page_preview' from reply payload


## 0.0.1 - 2018-04-14
### Added
- Initial source code
- This README file