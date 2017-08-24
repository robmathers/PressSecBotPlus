# PressSecBotPlus
### Contents
1. [About](#about)
2. [Requirements](#requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [License](#license)

## About
Inspired by [@realPressSecBot](https://twitter.com/realPressSecBot), PressSecBotPlus is a Python based Twitter bot that will reformat tweets by a specified user into a press release type image and publish it to Twitter.

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

## Requirements
- A Twitter API key, and an account from which to publish tweets
- Python 2.7 (should be compatible with Python 3, but I haven't done any testing)
- [python-twitter](https://github.com/bear/python-twitter)
- wkhtmltoimage, part of [wkhtmltopdf](https://wkhtmltopdf.org/)
- [Jinja2](http://jinja.pocoo.org)
- [Pillow](https://python-pillow.org)

## Installation
1. Install the requirements:
    - Download [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html), or install from your package manager
    - `pip install python-twitter Jinja2 Pillow` (`easy_install` also works)
2. [Download the source](https://github.com/robmathers/PressSecBotPlus/archive/master.zip) and unzip it (or clone the repository locally)
3. Set up a Twitter app
4. Copy `press_sec_bot_plus.conf.sample` to `press_sec_bot_plus.conf` and configure per the [Configuration section](#configuration)
5. *(Optional)* Install a user provided font; [instructions below](#fonts)
6. *(Optional)* If you wish to back-fill from existing tweets, add a section to the end of the config file, with a tweet ID as shown:

        [saved_state]
        last_tweet_id = 1234567890

    Everything *after* that tweet will be posted (in chronological order), up to a maximum of 200 tweets.

## Configuration
### Twitter API & Accounts
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
As PressSecBotPlus is intended to publish an ongoing stream of tweets, it is recommended that you run it as a daemon process. The best way of doing this will vary by OS. [Systemd for Ubuntu](https://wiki.ubuntu.com/SystemdForUpstartUsers), [Launchd for MacOS](https://alvinalexander.com/mac-os-x/mac-osx-startup-crontab-launchd-jobs), or [rc.d for FreeBSD](https://www.freebsd.org/doc/en/articles/rc-scripting/rcng-daemon.html) are suggested. Be careful to set the working directory to wherever `press_sec_bot_plus.py` is, as it expects other resources to be installed there.

Alternatively, you can run it as a background process using `screen` or similar.

PressSecBotPlus keeps track of the last Tweet it processed, so even if your daemon quits, it will resume from its last saved position upon restart.


### jQueryEmoji license
[jQueryEmoji][] is used in this code and is licensed under the following terms.

>(The MIT License)
>
>Copyright (c) by Rodrigo Polo [http://RodrigoPolo.com](http://RodrigoPolo.com)
>
>Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
>The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
>THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


[jQueryEmoji]: https://github.com/rodrigopolo/jqueryemoji
