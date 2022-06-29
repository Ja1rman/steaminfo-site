# -*- coding: utf-8 -*-

import requests
import re

steamid64ident = 76561197960265728

def fromURL(url):
    response = requests.get(url)
    page_html = response.text
    
    pattern = r'{"url":"(.*?)"'
    profile_url = re.findall(pattern, page_html)[0]
    profile_url = profile_url.replace('\\', '')

    pattern = r',"steamid":"(.*?)"'
    steam64 = re.findall(pattern, page_html)[0]

    permalink = 'https://steamcommunity.com/profiles/' + steam64

    pattern = r',"personaname":"(.*?)"'
    nick_name = re.findall(pattern, page_html)[0]

    pattern = r'data-miniprofile="(.*?)"'
    steam32 = re.findall(pattern, page_html)[0]

    steam3 = 'U:1:' + steam32

    steamidm = []
    steamidm.append('STEAM_0:')
    steamidacct = int(steam64) - steamid64ident
    
    if steamidacct % 2 == 0:
        steamidm.append('0:')
    else:
        steamidm.append('1:')
    
    steamidm.append(str(steamidacct // 2))

    steamid = ''.join(steamidm)

    xml = requests.get('https://steamcommunity.com/profiles/' + str(steam64) + '/?xml=1').text

    pattern = r"<vacBanned>(.*?)</vacBanned>"
    try: vacBanned = re.findall(pattern, xml)[0] 
    except: vacBanned = ' '

    pattern = r"<tradeBanState>(.*?)</tradeBanState>"
    try: tradeBanState = re.findall(pattern, xml)[0]
    except: tradeBanState = ' '

    pattern = r"<isLimitedAccount>(.*?)</isLimitedAccount>"
    try: isLimitedAccount = re.findall(pattern, xml)[0]
    except: isLimitedAccount = ' '

    pattern = r"<memberSince>(.*?)</memberSince>"
    try: memberSince = re.findall(pattern, xml)[0]
    except: memberSince = ' '

    return profile_url, permalink, nick_name, steam64, steam32, steamid, steam3, vacBanned, tradeBanState, isLimitedAccount, memberSince

def fromSTEAMid(steamid):
    sid_split = steamid.split(':')
    steam64 = int(sid_split[2]) * 2
    
    if sid_split[1] == '1':
        steam64 += 1
  
    steam64 += steamid64ident

    return fromURL('https://steamcommunity.com/profiles/' + str(steam64))

def from32id(steam32):
    return fromURL('https://steamcommunity.com/profiles/' + str( steamid64ident + int(steam32) ))

def check(steam32):
    response = requests.get('https://steamcommunity.com/id/' + steam32)
    page_html = response.text

    return 0 if page_html.find('<title>Steam Community :: Error</title>') == -1 else 1