# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import re
import urllib
import lxml.html
from lxml.cssselect import CSSSelector
dirname = "E:/H"
libname = "GREvI.xlsm"
def read_website(link):
	for i in range(3):
		try:
			f = urllib.urlopen(link)
			content = unicode(f.read(), "utf-8")
			return content
		except IOError:
			continue
	return None
def local_exist(directory, f):
	return os.path.exists(directory+f+".txt")
class Vocab:
	#------------------
	# .word
	#    The standard English spelling of the word.
	# .root
	#    The root of the word.
	# .mark
	#
	# .pronunciation
	#    Return the pronunciation of the word.
	#    If a local record does not exist, it will try to read from internet.
	# .chinese
	#    Return the Chinese meaning of the word.
	#    If a local record does not exist, it will try to read from internet.
	# .etymology
	#    Return the etymology of the word.
	#    If a local record does not exist, it will try to read from internet.
	# .english
	# .english_missing
	#    Return the boolean condition of an empty English meaning.
	def __init__(self, w, r=None, m=None, i=None, d=None, n=None, s=None, o=None):
		self.word = w
		self.root = r
		self.mark = m
		self.indx = i
		self.desc = d
		self.note = n
		self.synn = s
		self.ordr = o
		self.___p = None
		self.__cn = None
		self.__en = None
		self.etym = None
		self.skip = False
	def __str__(self):
		return w
	@property
	def dirdict(self):
		return dirname + "/dictionary/"
	@property
	def dirpron(self):
		return dirname + "/pronunciation/"
	@property
	def dirorig(self):
		return dirname + "/english/"
	@property
	def diretym(self):
		return dirname + "/etymology/"
	@property
	def is_common(self):
		return self.mark == 1
	def __save_to_localfile(self, directory, content):
		with open(directory+self.word+".txt", 'w') as f:
			f.write(content.encode('utf-8'))
	def __get_from_internet(self, link, selector):
		content = read_website(link)
		if content is not None:
			tree = lxml.html.fromstring(content)
			sel = CSSSelector(selector)
			results = sel(tree)
			return results
		return []

	@property
	def pronunciation(self):
		directory = self.dirpron
		if self.___p is None:
			if local_exist(directory, self.word):
				with open(directory+self.word+".txt", 'r') as f:
					p = f.read()
			else:
				p = self.__get_pronunciation_from_internet()
				self.__save_to_localfile(directory, p)
			self.___p = p
		return self.___p
	def __get_pronunciation_from_internet(self):
		x = ""
		link = "https://dictionary.cambridge.org/us/dictionary/english/"+self.word
		selector = 'span.us + span.uk span.ipa'
		for match in self.__get_from_internet(link, selector):
			x = "["+match.text_content()+"]"
			return x
		return x
	@property
	def chinese(self):
		directory = self.dirdict
		if self.__cn is None:
			if local_exist(directory, self.word):
				with open(directory+self.word+".txt", 'r') as f:
					chinese = f.read()
			else:
				chinese = self.__get_chinese_from_internet()
				self.__save_to_localfile(directory, chinese)
			self.__cn = chinese
		return self.__cn
	def __get_chinese_from_internet(self):
		x = ""
		link = "http://www.iciba.com/"+self.word
		selector = 'ul.base-list li'
		for match in self.__get_from_internet(link, selector):
			x += match.text_content().replace(" ","").replace("\n","")+"\n"
		return x
	@property
	def etymology(self):
		directory = self.diretym
		if self.etym is None:
			if local_exist(directory, self.word):
				with open(directory+self.word+".txt", 'r') as f:
					etymology = f.read()
			else:
				etymology = self.__get_etymology_from_internet()
				self.__save_to_localfile(directory, etymology)
			self.etym = etymology
		return self.etym
	def __get_etymology_from_internet(self):
		x = ""
		link = "https://www.etymonline.com/word/"+self.word
		selector = 'section object'
		for match in self.__get_from_internet(link, selector):
			x += match.text_content()+"\n"
		return x
	@property
	def english(self):
		directory = self.dirorig
		if self.__en is None:
			if local_exist(directory, self.word):
				with open(directory+self.word+".txt", 'r') as f:
					english = f.read()
			else:
				english = self.__get_english_from_internet()
				self.__save_to_localfile(directory, english)
			self.__en = ""
			for line in english.split('\n'):
				if len(line) == 0:
					continue
				indA = line.find(")")
				indB = line[1:].find("(")
				wordlist = re.findall('([a-zA-Z]+)', line[indA+1:indB])

				if self.word in wordlist:
					part = line[:indA+1]
					mean = line[indB+2:-2]
					self.__en += (part+mean+"\n")
			self.__en = english
		return self.__en
	def getEn(self):
		return self.__get_english_from_internet()
	def __get_english_from_internet(self):
		# x = ""
		# parameter = "sub=Search+WordNet&o2=&o0=1&o8=1&o1=1&o7=&o5=&o9=&o6=&o3=&o4=&h=0"
		# link = "http://wordnetweb.princeton.edu/perl/webwn?s=%s&%s"%(self.word, parameter)
		# selector = 'li'
		# for match in self.__get_from_internet(link, selector):
		# 	x += match.text_content().split("S: ")[1]+"\n"
		# return x
		x = ""
		link = "https://en.oxforddictionaries.com/definition/%s"%self.word
		selector = 'section.gramb'
		#sel = CSSSelector(selector)
		for match in self.__get_from_internet(link, selector):
			#results = sel(tree)
			ps = ""
			for pos in CSSSelector("span.pos")(match):
				ps = pos.text_content()
				break
			for m1 in CSSSelector("ul.semb li")(match):
				new_line = False
				for m2 in CSSSelector("span.ind")(m1):
					new_line = True
					x += "("+ps+")	"+m2.text_content()+"	"
					break
				for m3 in CSSSelector("div.exg div.ex")(m1):
					new_line = False
					x += " "+m3.text_content()+"\n"
					break
				if new_line:
					x += "\n"
		return x
	@property
	def english_missing(self):
		directory = self.dirorig
		if not local_exist(directory, self.word):
			self.english
		return os.path.getsize(directory+self.word+".txt") == 0
	def compare(self, reference):
		w = self.word
		r = reference
		max_size = len(w)
		for size in reversed(range(max_size+1)):
			for shift in range(max_size-size+1):
				substring = w[shift:shift+size]
				if len(substring) > 0 and substring in r:
					return substring
		return None
	@property
	def synonym(self):
		arr = []
		for l in self.english.split("\n"):
			la = l.find(") ")
			lb = l[la:].find("(")
			for single in l[la+1:lb+la].split(", "):
				single = single.strip()
				if single != self.word and len(single) > 1:
					arr.append(single)
		return "%s"%", ".join(set(arr))