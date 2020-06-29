from win32com.client import Dispatch
import os
silent = False

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

#speak = Dispatch("SAPI.SpVoice")

# speak_cn = Dispatch('SAPI.SpVoice')
# voice_list = speak_cn.GetVoices()
# voices = dict([(os.path.basename(voice.Id), voice) for voice in voice_list])
#print(voices)
#speak_cn.Voice = voices[u'TTS_MS_ZH-CN_HUIHUI_11.0']

def spell(content):
	if not silent:
		#speak_cn.Speak(content)
		engine.setProperty('voice', voices[0].id)
		engine.setProperty('rate', 120)
		engine.say(content)
		engine.runAndWait()

def english(content):
	if not silent:
		#speak_cn.Speak(content)
		engine.setProperty('voice', voices[0].id)
		engine.setProperty('rate', 175)
		engine.say(content)
		engine.runAndWait()

def chinese(content):
	if not silent:
		engine.setProperty('voice', voices[3].id)
		engine.setProperty('rate', 175)
		engine.say(content)
		engine.runAndWait()