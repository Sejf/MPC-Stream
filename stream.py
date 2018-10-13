# -*- coding: utf-8 -*-
import clipboard
import time
import subprocess
import re

providers = [
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?(?:youtube\.com/(?:(?:watch\?.*?(?:v=[^&\s]+))|(?:v/(?:.*)))|(?:youtu\.be(?:\.com)?/(?:.+?(?=\?)|.*))))",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?facebook\.com\/.*\/videos\/[0-9]*\/)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?vid\.me/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?dailymotion\.com\/(video|hub)\/([^_]+)[^#]*(#video=([^_&]+))?)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?vk\.com/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?streamable\.com/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?clips\.twitch\.tv/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?soundcloud\.com/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?openload\.co/embed/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?(?:go\.)?twitch\.tv/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?vimeo\.com/[0-9]*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?(?:pscp|periscope)\.tv/.*/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?twitter\.com/[a-z]*\/status(?:|es)/.*)",
    "(?:(?:.* |))((?:https?:\/\/)?(?:(?:(?:www\.)))?pornhub\.com\/view_video.php\?viewkey=[0-9]*)"]
#(?:(?:.* |))
lenregex = len(providers)
# Where you MPC player is
player = "C:\Program Files (x86)\K-Lite Codec Pack\MPC-HC64\mpc-hc64.exe"
# Youtube-DL path
youtubedl = "youtube-dl.exe"
provider = None
curclip = None
newclip = None
oldclip = None

def gclean(string):
    string = re.sub(r"b'",'',str(string))
    string = re.sub(r"b\"",'',str(string))
    string = re.sub(r"\\n'",'',str(string))
    string = re.sub(r"\\n\"",'',str(string))
    string = re.sub(r"\\x96",'-',str(string))
    return string

def extract(string, provider):
    string = re.match(providers[provider], string, re.IGNORECASE)
    string = string.group(1)
    return string

def check(string):
    if string is None:
        return (False)
    elif string == oldclip:
        return (False)
    else:
        return (True)

def match(string):
    varcount = lenregex
    i = 0
    while i != varcount:
        matchclipboard = re.match(providers[i], string, re.IGNORECASE)
        if matchclipboard is not None:
            provider = providers[i]
            return (True, provider)
        i += 1
        if (i >= varcount):
            return (False, False)

def titlextract(clipboard):
    clipboard = [youtubedl, "-e", clipboard]
    clipboard = str(subprocess.check_output(clipboard))
    clipboard = gclean(clipboard)
    return (clipboard)

def play(clipboard, provider):
    url= None
    error = False
    if provider == providers[0]:
        clipboard = extract(clipboard,0)
        geturl = [youtubedl, clipboard, "-f best[height<=720p]", "-g"]
    elif provider == providers[1]:
        clipboard = extract(clipboard,1)
        geturl = [youtubedl, clipboard, "-f best", "-g"]
    else:
        geturl = [youtubedl, clipboard, "-g", "--netrc"]
    try:
        url = str(subprocess.check_output(geturl))
    except subprocess.CalledProcessError:
        error = True
    if error == False:
        url = gclean(url)
        url = [player, url, "/play"]
        subprocess.Popen(url)
        title = titlextract(clipboard)
        print("▓",title,"\n",clipboard)
        #print(clipboard)

while True:
    newclip = clipboard.paste()
    if check(newclip) == True:
        bol,provider = match(newclip)
        if (bol == True):
            oldclip = newclip
            play(newclip, provider)
    # How Many time (in seconds) between scans        
    time.sleep(1)
