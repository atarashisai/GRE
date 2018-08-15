from win32com.client import Dispatch
import os
silent = False
speak = Dispatch("SAPI.SpVoice")

speak_cn = Dispatch('SAPI.SpVoice')  
voice_list = speak_cn.GetVoices()
voices = dict([(os.path.basename(voice.Id), voice) for voice in voice_list])  
#speak_cn.Voice = voices['TTS_MS_ZH-CN_HUIHUI_11.0']

def english(content):
	if not silent:
		speak.Speak(content)

def chinese(content):
	if not silent:
		speak_cn.Speak(content)