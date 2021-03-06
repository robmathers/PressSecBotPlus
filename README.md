# PressSecBotPlus
### Contents
1. [About](#about)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [License](#license)

## About
Inspired by [@realPressSecBot](https://twitter.com/realPressSecBot), PressSecBotPlus is a Python based Twitter bot that will reformat tweets by a specified user into a press release image and publishes to Twitter.

While the major function is similar, there are some specific enhancements over @realPressSecBot. The goal is to provide more context by including emoji, images and video from the original tweet, as well as a more mobile-friendly reading experience. Statements are formatted for narrower screens, and rendered at higher resolution for Retina screens.

### Improvements on @realPressSecBot
- Mobile-friendly presentation
- High-DPI rendering
- Images from original tweet are included (up to 3 due to Twitter limits; extras are linked)
- Video or GIF from original tweet are noted and linked
- Long URLs are formatted to be readable within the visible statement
- Emoji are displayed properly (using [jQueryEmoji][])
- Statements are published to Twitter as PNGs to avoid compression artifacts

### To-do list
- Clickable links
- Inline Twitter full name expansion
- Quoted tweet formatting
- Use the Twitter Streaming API for real-time updates, rather than polling

### Samples
<img src="sample.png" width="375px" alt="Sample press release image">
<a href="https://twitter.com/dog_rates"><img src="sample2.jpg" width="375px" alt="Sample full tweet"></a>

## Requirements
- A Twitter API key, and an account from which to publish tweets
- Python 2.7 (should be compatible with Python 3, but I haven't done any testing)
- [python-twitter](https://github.com/bear/python-twitter)
- wkhtmltoimage, part of [wkhtmltopdf](https://wkhtmltopdf.org/)
- [Jinja2](http://jinja.pocoo.org)
- [Pillow](https://python-pillow.org)

## Installation
1. Install the requirements:
    - [Download wkhtmltopdf][], or install from your package manager
    - `pip install python-twitter Jinja2 Pillow` (`easy_install` also works)
2. [Download the source][source] and unzip it (or clone the repository locally)
3. Set up a Twitter app
    - Follow the [Python-twitter instructions][app-keys] to create an app and get your API keys and access tokens
    - If you want to register your app with a different account than the one your bot will tweet from, use the [`get_access_token.py`][token] script to get the access tokens for the bot's account
4. Copy `press_sec_bot_plus.conf.sample` to `press_sec_bot_plus.conf` and configure per the [Configuration section](#configuration)
5. *(Optional)* Install a user provided font; [instructions below](#fonts)
6. *(Optional)* If you wish to back-fill from existing tweets, add a section to the end of the config file, with a tweet ID as shown:

        [saved_state]
        last_tweet_id = 1234567890

    Everything *after* that tweet will be posted (in chronological order), up to a maximum of 200 tweets.

[download wkhtmltopdf]: https://wkhtmltopdf.org/downloads.html
[source]: https://github.com/robmathers/PressSecBotPlus/archive/master.zip
[app-keys]: https://python-twitter.readthedocs.io/en/latest/getting_started.html
[token]: https://github.com/bear/python-twitter/blob/master/get_access_token.py

## Configuration
### Twitter API & accounts
In the `settings` section of `press_sec_bot_plus.conf`:

- Enter the username of the account you wish to create releases for (@ sign optional)
- Enter the text you wish to prefix each tweet with (no quotes necessary); to have no text, delete the placeholder or the whole line (`message = TWEET_STATUS_TEXT_HERE`)

In the `twitter_api` section, enter your Twitter API credentials as labelled.

### Fonts
PressSecBotPlus will use typefaces in the following order:

1. A user-provided font, loaded via a `font.css` file
2. The Palatino typeface, if it is installed locally (this best matches traditional White House releases)
3. The fallback serif typeface on the system

#### User-provided font
To use a font of your choosing, create a `font.css` file in your directory, containing a CSS `@font-face` directive. Use the [`src` descriptor][src] to load the font, but the `font-family` **must be set to `import`**.

[Transfonter][] can help you generate proper `@font-face` files. If generated with the base64 option, the font will be embedded in the `stylesheet.css` you download. Rename that to `font.css`, and set the `font-family` to `import` on *all* the rules (there may be more than one, for multiple weights/styles).

For more details, read the [`@font-face` documentation][font-face].

[src]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/src
[transfonter]: https://transfonter.org
[font-face]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face


## Usage
Run PressSecBotPlus with `python press_sec_bot_plus.py` , or first mark it as executable with `chmod +x press_sec_bot_plus.py`, then run `./press_sec_bot_plus.py`.

When run, PressSecBotPlus publishes any tweets since the last one it re-published, in proper chronological order. It will then check every five minutes for new tweets, until you quit.

### Running as a daemon process
As PressSecBotPlus is intended to publish an ongoing stream of tweets, it is recommended that you run it as a daemon process. The best way of doing this will vary by OS. [Systemd for Ubuntu], [Launchd for MacOS][], or [rc.d for FreeBSD][] are suggested. Be careful to set the working directory to wherever `press_sec_bot_plus.py` is, as it expects other resources to be installed there.

[systemd for ubuntu]: https://wiki.ubuntu.com/SystemdForUpstartUsers
[launchd for macos]: https://alvinalexander.com/mac-os-x/mac-osx-startup-crontab-launchd-jobs
[rc.d for freebsd]: https://www.freebsd.org/doc/en/articles/rc-scripting/rcng-daemon.html

Alternatively, you can run it as a background process using `screen` or similar.

PressSecBotPlus keeps track of the last Tweet it processed, so even if your daemon quits, it will resume from its last saved position upon restart.

## License
PressSecBotPlus is Copyright © 2017 by Rob Mathers and licensed under the MIT license. You may do what you like with the software, but must include the [license and copyright notice](https://github.com/robmathers/PressSecBotPlus/blob/master/LICENSE.txt).

### jQueryEmoji license
[jQueryEmoji](https://github.com/rodrigopolo/jqueryemoji) is used in this code and is Copyright (c) by Rodrigo Polo [http://RodrigoPolo.com](http://RodrigoPolo.com) and licensed under the MIT License.
