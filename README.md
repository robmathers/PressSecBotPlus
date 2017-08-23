# PressSecBotPlus
## About
Inspired by [@realPressSecBot](https://twitter.com/realPressSecBot), PressSecBotPlus is a Python based Twitter bot that will reformat tweets by a specified user into a press release type image and publish it to Twitter.

While the major function is similar, there are some specific enhancements over @realPressSecBot. The goal is to provide more context by including images and video from the original tweet, as well as a more mobile-friendly reading experience. Statements are formatted for narrower screens, and rendered at higher resolution.

### Improvements on @realPressSecBot
- Mobile-friendly presentation
- High-DPI rendering
- Images from original tweet are included (up to 3 due to Twitter limits; extras are linked)
- Video or GIF from original tweet are noted and linked
- Long URLs are formatted to be readable within the visible statement
- Emoji are displayed properly (using [jQueryEmoji][])
- Statements are published to Twitter as PNGs to avoid JPEG text compression artifacts

### To-do list
- Clickable links
- Inline Twitter full name expansion
- Quoted tweet formatting

## Requirements
- A Twitter API key, and an account from which to publish tweets
- Python 2.7 (should be compatible with Python 3, but I haven't done any testing)
- [python-twitter](https://github.com/bear/python-twitter)
- wkhtmltoimage, part of [wkhtmltopdf](https://wkhtmltopdf.org/)
- [Jinja2](http://jinja.pocoo.org)
- [Pillow](https://python-pillow.org)

## Installation
1. Install the requirements:
    - `pip install python-twitter Jinja2 Pillow`
    - Download [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html), or install from your package manager
2. Download the source
3. Set up a Twitter app
4. Edit the config file
5. Set up a daemon process

## Configuration
### Twitter API & Accounts



### Fonts
PressSecBotPlus will use typefaces in the following order:

1. The Palatino typeface, if it is installed locally (this best matches traditional White House releases)
2. A user-provided font, loaded via a `font.css` file
3. The fallback serif typeface on the system

#### User-provided font
To use a font of your choosing, create a `font.css` file in your directory, containing a CSS `@font-face` directive. Use the [`src` descriptor][src] to load the font, but the `font-family` **must be set to `import`**.

[Transfonter][] can help you generate proper `@font-face` files, just rename `stylesheet.css` to `font.css`, and set the `font-family` to `import` on *all* the rules (there may be more than one, for multiple weights/styles).

For more details, read the [`@font-face` documentation][font-face].

[src]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face/src
[transfonter]: https://transfonter.org
[font-face]: https://developer.mozilla.org/en-US/docs/Web/CSS/@font-face


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
