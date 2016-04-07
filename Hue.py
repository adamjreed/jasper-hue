# -*- coding: utf-8-*-
import re
import requests
import logging

WORDS = ["TURN LIGHT"]
TOGGLE_STATE = re.compile('turn (the )?([\w\s]+) lights (on|off)', re.IGNORECASE)
SET_BRIGHTNESS = re.compile('set (the)?([\w\s]+) lights to (quarter|half|(three quarter)|full) brightness', re.IGNORECASE)

class Hue:
    def __init__(self, mic, profile):
        self.profile = profile
        self.mic = mic
        self.base_url = 'http://' + profile['hue']['bridge_ip'] + '/api/' + profile['hue']['user']
        self.brightness_levels = {
            'quarter': '64',
            'half': '128',
            'three quarter': '196',
            'full': '254'
        }

        self._logger = logging.getLogger(__name__)

    def toggleState(self, regex):
        roomId = self.getRoomId(regex.group(2).lower())
        state = regex.group(3).lower()

        if(state == 'on'):
            state = 'true'
            bri = '254'
        else:
            state = 'false'
            bri = '0'

        url = self.base_url + '/groups/' + roomId +'/action'
        body = '{"on":' + state + ', "bri":' + bri + '}'

        r = requests.put(url, body)

        r.raise_for_status();

    def setBrightness(self, regex):
        roomId = self.getRoomId(regex.group(2).lower())
        bri = regex.group(3).lower()

        if bri not in self.brightness_levels:
            self.mic.say("Sorry, that is not a valid brightness level. Valid levels are quarter, hald, three quarter, and full.")
            return

        url = self.base_url + '/groups/' + roomId + '/action'
        body = '{"on":true ' + ', "bri":' + self.brightness_levels[bri] + '}'

        r = requests.put(url, body)

        r.raise_for_status();

    def getRoomId(self, room):
        #TODO: write a script to get this info from the Hue bridge and add it to the profile
        rooms = {'bedroom': '1'}

        return rooms[room]

def handle(text, mic, profile):
    hue = Hue(mic, profile)

    toggle_state = TOGGLE_STATE.match(text)
    if(bool(toggle_state)):
        hue.toggleState(toggle_state)
        return
    
    set_brightness = SET_BRIGHTNESS.match(text)
    if(bool(set_brightness)):
        hue.setBrightness(set_brightness)
        return

    mic.say("I'm sorry, that didn't appear to be a valid Hue command.")

def isValid(text):
    """
        Returns True if the input is related to the meaning of life.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(TOGGLE_STATE.search(text)) | bool(SET_BRIGHTNESS.search(text))