# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, make_response, redirect, url_for, flash
from steamid import *

application = Flask(__name__)


@application.route('/', methods=['GET', 'POST'])
@application.route('/steamid/', methods=['GET', 'POST'])
def page_source():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        user_text = request.form['text']

        return return_info(user_text)


@application.route('/steamid/<username>/', methods=['GET'])
def get_steam_id(username=None):
    return return_info(username)


def return_info(user_text):
    try:
        user_text = user_text.replace(' ', '')

        if user_text.lower().startswith('https://') or user_text.lower().startswith('http://'):
            values = fromURL(user_text)
        elif user_text.upper().startswith('STEAM_0:'):
            values = fromSTEAMid(user_text)
        elif user_text.upper().startswith('U:1:'):
            values = from32id(user_text[4:])
        elif user_text.startswith('7656') and len(user_text) == 17:
            values = fromURL(
                'https://steamcommunity.com/profiles/' + user_text)
        elif check(user_text):
            values = from32id(user_text)
        else:
            values = fromURL('https://steamcommunity.com/id/' + user_text)

        profile_url, permalink, nick_name, steam64, steam32, steamid, steam3, vacBanned, tradeBanState, isLimitedAccount, memberSince = values

        return render_template('index.html', user_text=user_text, profile_url=profile_url,
                               permalink=permalink, nick_name=nick_name, steam64=steam64, 
                               steam32=steam32, steamid=steamid, steam3=steam3, 
                               vacBanned=vacBanned, tradeBanState=tradeBanState, 
                               isLimitedAccount=isLimitedAccount, memberSince=memberSince)
    except:
        return render_template('index.html', user_text=user_text, error='error')

if __name__ == '__main__':
    application.run(host='0.0.0.0')
