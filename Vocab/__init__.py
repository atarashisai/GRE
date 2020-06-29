# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import logging
import Reader
import time
import opencc
cc = opencc.OpenCC('s2t')
logging.basicConfig(filename='word.log',level=logging.INFO, format="%(message)s")

def printf(anything):
	print(anything)
	logging.info(anything)

def transcribe_pronunciation(spelling):
	'''
	This function transcribes the pronunication 
		from IPA to phonetic symbols.
	'''
	def match(begin, original, pattern):
		pattern_array = list(pattern)
		size = len(pattern_array)
		if (size > len(original) - begin):
			return False
		for offset in range(0, size):
			if (original[begin+offset] != pattern_array[offset]):
				return False
		return True

	def modify(begin, original, size, wish):
		for offset in range(1, size):
			original[begin+offset] = ''
		original[begin+0] = wish
		return size-1
	'''
	'''
	all_sound = spelling.split(' | ')
	if len(all_sound) == 4:
		spelling = min(all_sound, key=len)
	array = ['\n']+list(spelling)
	array.append('\n')
	skip_counter = 0
	maxlen = len(array)
	for i in range(0, maxlen):
		if skip_counter > 0:
			skip_counter -= 1
			continue
		for each in [
			(u'\ndʒ' ,u'\nj'),
			(u'dʒi\n'  ,u'dji\n'),
			(u'i\n'  ,u'y\n'),
			(u'ɪk\n'  ,u'ɪc\n'),
			(u'ŋɡ' ,u'ng'),
			(u'ŋk' ,u'nk'),
			(u'ŋ'  ,u'ng'),
			(u'ɡ'  ,u'g'),
			(u'æ'  ,u'ä'),
			(u'ʌ'  ,u'u'),
			(u'ɔːr',u'or'),
			(u'ɔː' ,u'au'),
			(u'ɒ'  ,u'o'),
			(u'əʊ' ,u'əw'),
			(u'əʊ' ,u'əw'),
			(u'oʊ' ,u'əw'),
			(u'aʊ' ,u'ou'),
			(u'ʊr' ,u'oor'),
			(u'ɑːr',u'ar'),
			(u'ɑː' ,u'o'),
			(u'ɑ'  ,u'o'),
			(u'iː' ,u'ee'),
			(u'uː' ,u'oo'),
			(u'ɔɪ' ,u'oy'),
			(u'aɪ' ,u'ei'),
			(u'eɪ' ,u'ay'),
			(u'ˈju',u'eu'),
			(u'ˈjʊ',u'eu'),
			(u'ju' ,u'ew'),
			(u'jʊ' ,u'ew'),
			(u'ɜːr',u'ər'),
			(u'əːr',u'ər'),
			(u'ɪr' ,u'eer'),
			(u'ɪər' ,u'eer'),
			(u'er' ,u'air'),
			(u'ˈdʒ',u'ˈj'),
			(u'dʒ' ,u'dj'),
			(u'tʃʊ' ,u'chw'),
			(u'tʃ' ,u'ch'),
			(u'ʃn',u'tion'),
			(u'ʃən',u'tion'),
			(u'ʒn' ,u'zion'),
			(u'ʒən' ,u'zion'),
			(u'ʃ\n'  ,u'sch\n'),
			(u'ʃ'  ,u'sh'),
			(u'j'  ,u'y'),
			(u'a'  ,u'ä'),
			(u'ː'  ,u''),
		]:
			pattern = each[0]
			target  = each[1]
			if match(i, array, pattern):
				skip_counter = modify(i, array, len(pattern), target)
				break
	sound = ''.join(array)[1:-1]
	if len(sound) > 1 and sound[0] == 'ˈ':
		sound = sound[1:]
	return sound

class Vocab:
	def __init__(self, word, data, rank=""):
		pr = '1'
		en = '2'
		cn = '3'
		tg = '4'
		self.word = word
		self.part = None
		self.rank = rank
		if not data:
			self.__en = {}
			self.__cn = {}
			self.__pr = "???"
		else:
			self.__en = data[en]
			self.__cn = data[cn]
			self.__pr = transcribe_pronunciation(data[pr])

	@property
	def exist(self):
		return bool(self.__en)

	@property
	def english(self):
		return self.__en

	@property
	def chinese(self):
		return self.__cn
	
	@property
	def pronunciation(self):
		return self.__pr

	def set_part(self, part):
		self.part = part

	def print_part(self, p):
		word = self.word
		sound = self.pronunciation
		#chinese = ""
		chinese = self.chinese
		sound = "*"+sound+"	"#+" :: "
		splitter = u'	'+self.rank+u'	'#u'　'

		if p == 'abbreviation':
			printf(word.upper()+'.'+splitter)
			return
		if p == 'pronoun':
			if 'pron.' in chinese:
				splitter += chinese['pron.'].replace(u'，', u'；').split(u'；')[0]+u"。"
				splitter = cc.convert(splitter)
			printf(sound+word+splitter)
			if 'pron.' in chinese:
				print(chinese['pron.'])
			return
		if p == 'proper noun':
			printf(sound+word.capitalize()+splitter)
			return
		if p == 'noun':
			if 'n.' in chinese:
				splitter += chinese['n.'].replace(u'，', u'；').split(u'；')[0]+u"。"
				splitter = cc.convert(splitter)
			if word[0] in ['a', 'e', 'i', 'o']:
				printf(sound+'an '+word+splitter)
			else:
				printf(sound+'a '+word+splitter)
			if 'n.' in chinese:
				print(chinese['n.'])
			return
		if p == 'verb':
			for key in ['vt.', 'vi.', 'v.', 'vt.&vi.']:
				if key in chinese:
					splitter += chinese[key].replace(u'，', u'；').split(u'；')[0]+u"。"
					splitter = cc.convert(splitter)
					break
			printf(sound+'to '+word+splitter)
			for key in ['vt.', 'vi.', 'v.', 'vt.&vi.']:
				if key in chinese:
					print(chinese[key])
			return
		if p == 'adjective':
			if 'adj.' in chinese:
				splitter += chinese['adj.'].replace(u'，', u'；').split(u'；')[0]+u"。"
				splitter = cc.convert(splitter)
			printf(sound+'be '+word+splitter)
			if 'adj.' in chinese:
				print(chinese['adj.'])
			return
		if p == 'adverb':
			if 'adv.' in chinese:
				splitter += chinese['adv.'].replace(u'，', u'；').split(u'；')[0]+u"。"
				splitter = cc.convert(splitter)
			printf(sound+word+', '+splitter)
			if 'adv.' in chinese:
				print(chinese['adv.'])
			return
		printf(sound+p+" "+word+splitter)

	def pprint(self, title_only=False):
		#print(data)
		#print(word+" [ "+transcribe_pronunciation(data[__pr])+" ]")
		print(self.word)
		if self.part != None:
			if self.part in self.english:
				self.print_part(self.part)
			else:
				printf("*??	"+self.word)
			return
		for p, m in self.english.items():
			if self.part == None:
				self.print_part(p)
			if title_only:
				continue
			for each in m:
				if len(each['s']) > 0:
					print('* ['+each['s']+'] '+each['m'])
				else:
					print('* '+each['m'])
				sentence = each['e']
				if len(sentence) > 0:
					if sentence[-1] not in ['!', '?', '.']:
						print(' '*4+sentence[0].capitalize()+sentence[1:]+'.')
					else:
						print(' '*4+sentence[0].capitalize()+sentence[1:])
				if len(each['c']) > 0:
					print(each['c']+u'。')
			print('-'*17)