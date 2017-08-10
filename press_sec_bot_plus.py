#!/usr/bin/env python
import sys
from datetime import date
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError
from subprocess import Popen, PIPE
from distutils.spawn import find_executable
from tempfile import NamedTemporaryFile
import twitter
import jinja2

config_file='press_sec_bot_plus.conf'

def load_config():
    global config_file
    config = SafeConfigParser()
    if not config.read(config_file):
        print "Couldn't load configuration."
        sys.exit(1)

    return config


def save_config(config):
    with open(config_file, 'w') as f:
        config.write(f)


def save_last_tweet(config, tweet_id):
    if not config.has_section('saved_state'):
        config.add_section('saved_state')
    config.set('saved_state', 'last_tweet_id', str(tweet_id))
    save_config(config)


def api_from_config(config):
    api = twitter.Api(
        consumer_key=config.get('twitter', 'consumer_key'),
        consumer_secret=config.get('twitter', 'consumer_secret'),
        access_token_key=config.get('twitter', 'access_token_key'),
        access_token_secret=config.get('twitter', 'access_token_secret'),
        tweet_mode='extended')

    return api

def render_tweet_html(tweet):
    date_format = '%B %-d, %Y'
    context = {
        'body': process_tweet_text(tweet),
        'date': date.fromtimestamp(tweet.created_at_in_seconds).strftime(date_format)
    }
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader('./')
    ).get_template('release_template.html').render(context)


def process_tweet_text(tweet):
    text = tweet.full_text

    for url in tweet.urls:
        text = text.replace(url.url, url.expanded_url)

    for media in tweet.media or []:
        text = text.replace(media.url, '')

    return jinja2.Markup(text.replace('\n', '<br>').strip())


def html_to_png(html):
    command = ['wkhtmltoimage']
    if not find_executable(command[0]):
        raise ImportError('%s not found' % command[0])

    command += ['-f', 'png'] # format output as PNG
    command += ['--zoom', '2'] # retina image
    command += ['--width', '750'] # viewport 750px wide
    command += ['-'] # read from stdin
    command += ['-'] # write to stdout

    wkhtml_process = Popen(command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    (output, err) = wkhtml_process.communicate(input=html.encode('utf-8'))

    output = set_retina_dpi(output)

    return output


def set_retina_dpi(png_bytes):
    command = ['convert']
    if not find_executable(command[0]):
        raise ImportError('ImageMagick not found')

    command += ['-units', 'PixelsPerInch']
    command += ['-density', '144'] # 144 seems to be required for Preview to show @2x
    command += ['-', '-'] # read and write to provided file_path

    convert_process = Popen(command, stdin=PIPE, stdout=PIPE)
    (output, err) = convert_process.communicate(input=png_bytes)

    return output

def release_tweet(tweet, api):
    """Formats and publishes a Tweet to the account"""
    tweet_html = render_tweet_html(tweet)
    image_data = html_to_png(tweet_html)

    status = ''
    media = []

    # Max 4 photos, or 1 video or 1 GIF

    for media_item in tweet.media or []:
        extra_media_url = 'https://twitter.com/%s/status/%d' % (tweet.user.screen_name, tweet.id)
        if media_item.type == 'video':
            status = '[Video: %s]' % extra_media_url

        if media_item.type == 'animated_gif':
            status = '[GIF: %s]' % extra_media_url

        if media_item.type == 'photo':
            if len(media) < 3:
                media.append(media_item.media_url_https)

                # Use large photo size if available
                if media_item.sizes.has_key('large'):
                    media[-1] += ':large'
            else:
                if status != '':
                    status += '\n'
                status += '[Photo: %s]' % extra_media_url

    print status
    print media

    with NamedTemporaryFile(suffix='.png') as png_file:
        png_file.write(image_data)
        media.insert(0, png_file)
        api.PostUpdate(status=status, media=media)


def poll_for_updates(api, account_to_follow, starting_id=None, interval=300):
    """Gets new tweets and releases them every interval (seconds).
    If starting_id is provided, the initial run will start with all tweets since that id, up to a maximum of 200."""
    from time import sleep

    latest_tweet_id = starting_id or api.GetUserTimeline(screen_name=account_to_follow, count=1)[0].id
    while True:
        new_tweets = api.GetUserTimeline(screen_name=account_to_follow, since_id=latest_tweet_id, count=200, include_rts=False)

        # process the list in reverse order, to preserve time-order
        for tweet in new_tweets[::-1]:
            release_tweet(tweet, api)

        if len(new_tweets) > 0:
            latest_tweet_id = new_tweets[0].id
            save_last_tweet(load_config(), latest_tweet_id)

        sleep(interval)


def main():
    config = load_config()
    api = api_from_config(config)

    account_to_follow = config.get('settings', 'account_to_follow')

    try:
        last_tweet_id = int(config.get('saved_state', 'last_tweet_id'))
    except (NoOptionError, NoSectionError) as e:
        last_tweet_id = None

    poll_for_updates(api, account_to_follow, last_tweet_id)

if __name__ == "__main__":
    main()
