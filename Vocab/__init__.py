# -*- coding: utf-8 -*-
from __future__ import print_function

import xlrd
import time
from web import get_pronunciation
from web import get_english
from web import get_chinese
from web import update_from_web
from web import update_from_local
import logging
logging.basicConfig(filename='word.log',level=logging.INFO, format="%(message)s")

class Vocab:
	def __init__(self, w, s=None, c=None, r=0, f="", p="", m=None, cn=None):
		self.word = w
		self.__pr = get_pronunciation(self.word, L1only=True).replace("(ə)", "ə")
		self.__en = None
		self.__cn = None
		self.__ck = c
		self.rank = r
		self.form = f
		self.mean = m
		self.part = p
		self.chns = cn

	@property
	def pronunciation(self):
		if self.__pr is None:
			self.__pr = get_pronunciation(self.word)
			return self.__pr
		else:
			return self.__pr

	@property
	def english(self):
		if self.__en is None:
			self.__en = []
			for each in get_english(self.word).split("\n"):
				count = len(each)
				if count > 0:
					self.__en.append(Acceptation(each))
			return self.__en
		else:
			return self.__en

	@property
	def chinese(self):
		if self.__cn is None:
			self.__cn = get_chinese(self.word)
			return self.__cn
		else:
			return self.__cn

	@property
	def checked(self):
		return self.__ck

class Acceptation:
	def __init__(self, english):
		p,s,m,e = english.split("\t")

		self.part = self.abbrev(p)
		self.subject = s
		self.meaning = m
		self.example = e

	def abbrev(self, part):
		# if part == "(noun)"			: return "(n)"
		# if part == "(pronoun)"		: return "(n)"
		# if part == "(abbreviation)"	: return "(a)"
		return part.upper()
	@property
	def p(self):
		return self.part

	@property
	def s(self):
		return self.subject

	@property
	def m(self):
		return self.meaning

	@property
	def e(self):
		return self.example

'''
	class
	---------------------------
	module
'''
def p_chinese(vocab, delay=0.5,skip=False):
	if skip:
		en = vocab.english
		return
	title = "%s  /%s/"%(vocab.word, vocab.pronunciation)
	print("\n"+title+"\n"+vocab.chinese+"\n")

def update(vocab, delay=0.5,skip=False, part=None):
	update_from_web(vocab.word)
	p(vocab, delay, skip, part)

def local_update(vocab, delay=0.5,skip=False, part=None):
	update_from_local(vocab.word)
	p(vocab, delay, skip, part)

def review(vocab, delay=0.5):
	title = "%s: %s  |  %s"%(vocab.part[0], vocab.word.ljust(15), vocab.pronunciation)
	print("-"*40)
	print(title)
	print(vocab.chns+"；"+vocab.mean)
	time.sleep(delay)

def p(vocab, delay=0.5,skip=False,part=None, update=False):
	if skip:
		en = vocab.english
		return
	if update:
		if vocab.pronunciation is "" or vocab.pronunciation is None:
			print(vocab.word)
			print(vocab.pronunciation)
			update_from_web(vocab.word)
			#time.sleep(1)
		return
		if vocab.pronunciation is "":
			print("100000	"+vocab.word)
			return
		else:
			if vocab.rank == "" or vocab.rank > 999990:
				print("	"+vocab.word)
			else:
				print("%d	"%vocab.rank+vocab.word)
			return
		#pass
	chinese = {}
	for cn in vocab.chinese.split("\n"):
		if len(cn) < 1:
			continue
		dot = cn.find('.')
		p = cn[0:dot]
		if p == "n":
			chinese["(NOUN)"]=cn
		if p == "pron":
			chinese["(PRONOUN)"]=cn
		if p == "v" or p == "vi" or p == "vt":
			chinese["(VERB)"]=cn
		if p == "adj":
			chinese["(ADJECTIVE)"]=cn
		if p == "adv":
			chinese["(ADVERB)"]=cn
	padding = ""
	if len(vocab.pronunciation) > 1 and vocab.pronunciation[0] == "ˈ":
		padding = "ˈ"
	all_p = {}
	for each in vocab.english:
		if each.p not in all_p:
			all_p[each.p] = []
		line = ""
		line += each.m
		if len(each.s) > 0:
			line += " -- used in "+each.s
		line += "\n  "
		if len(each.e) > 0:
			line += each.e
		all_p[each.p].append(line)
	for p, all_m in all_p.items():
		if (part is not None) and (p != part):
			continue
		if vocab.part in ("NOUN", "VERB", "ADJECTIVE", "ADVERB"):
			if vocab.part not in p:
				continue
		#print(p,part,(part is not None),(p != part))
		# if len(vocab.form) < 1:
		# 	title = "%s%s\n%s"%(padding, vocab.word, vocab.pronunciation)
		# else:
		# 	title = "%s%s\n%s"%(padding, vocab.form, vocab.pronunciation)
		print("-"*40)
		if p == "(ABBREVIATION)":
			title = "%s: %s  |  %s"%(p[1], vocab.word.upper().ljust(15), vocab.pronunciation)
		elif p == "(PROPER NOUN)":
			title = "%s: %s  |  %s"%(p[1], vocab.word.capitalize().ljust(15), vocab.pronunciation)
		elif p == "(VERB)":
			title = " to %s  |  %s"%(vocab.word.ljust(15), vocab.pronunciation)
		elif p == "(NOUN)":
			title = "the %s  |  %s"%(vocab.word.ljust(15), vocab.pronunciation)
		elif p == "(ADJECTIVE)":
			title = " be %s  |  %s"%(vocab.word.ljust(15), vocab.pronunciation)
		else:
			title = "%s: %s  |  %s"%(p[1], vocab.word.ljust(15), vocab.pronunciation)
		print(title)
		logging.info(title)
		if vocab.chns is not None and len(vocab.chns) > 0:
			chinese[p] = vocab.chns
		if p in chinese:
			print("> "+chinese[p]+" <")
			logging.info(chinese[p])
		if vocab.mean is not None:
			print(vocab.mean)
			logging.info(vocab.mean)
			time.sleep(delay*vocab.mean.count(' '))
		n = 0
		for m in all_m:
			n += 1
			#print(("%s..."%n)+m)
			#time.sleep(delay*m.count(' '))
			sentence = m.split("    ")
			if len(sentence) < 2:
				sentence.append("")
			logging.info(sentence[0])
			if len(sentence[1]) > 1:
				print(("%s..."%n)+sentence[1])
				time.sleep(delay*sentence[1].count(' ')+1)
				logging.info(sentence[1])
		logging.info("....")
	return ""
def withdraw_all(dirxlsm, ind=0, row=1, review=False): #>> {"word":cols}
	workbook = xlrd.open_workbook(dirxlsm)
	sheet = workbook.sheet_by_index(ind)
	pool = []
	for rowx in range(sheet.nrows):
		if rowx < row:
			continue
		cols = sheet.row_values(rowx)
		wrd = cols[0] #Word
		rnk = cols[1] #Rank
		prn = cols[2] #Pronunciation
		chk = cols[3] #Checked
		frm = cols[4] #Formation
		chn = cols[5] #Formation
		prt = cols[6] #Formation
		mng = cols[7] #Formation
		if len(wrd) < 1:
			continue
		if wrd[0] == '*':
			wrd = wrd[1:]
		if review and chk == 1.0:
			pool.append(Vocab(wrd, prn, chk, rnk, frm, prt, mng, chn))
		elif review == False and chk != 1.0:
			pool.append(Vocab(wrd, prn, chk, rnk, frm, prt, mng, chn))
	return pool

def withdraw_all_old(dirxlsm, ind=0, row=2): #>> {"word":cols}
	workbook = xlrd.open_workbook(dirxlsm)
	sheet = workbook.sheet_by_index(ind)
	pool = []
	for rowx in range(sheet.nrows):
		if rowx < row:
			continue
		cols = sheet.row_values(rowx)
		w = cols[2] #Word
		r = cols[4] #Rank
		p = None #Pronunciation
		c = cols[3] #Checked
		f = cols[2] #Formation
		if len(w) < 1:
			continue
		if w[0] == '*':
			w = w[1:]
		pool.append(Vocab(w, p, c, r, f))
	return pool