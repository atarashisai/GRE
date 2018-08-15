# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import sqlite3
import xlrd
import time
import random
import Reader
import json
import Database
from Database import Vocab
Database.dirname = os.path.dirname(Database.__file__)

dirxlsm=os.path.dirname(Database.dirname)+"/Category.19.xlsm"
cnt = 0
delay = 0
import logging
logging.basicConfig(filename='word.log',level=logging.INFO)

def collec():
	link = {}
	directory = Database.dirname+"/pronunciation"
	for filename in os.listdir(directory):
		if filename.endswith(".txt"): 
			path = os.path.join(directory, filename)
			if os.path.getsize(path) > 0:
				with open(path, 'r') as f:
					link[filename[:-4]] = f.read()
		else:
			continue
	with open(Database.dirname+'/pronunciation.json', 'w') as f:
		json.dump(link, f)
def p(vocab, etymology=False):
	if len(vocab.pronunciation) > 3:
		print(vocab.pronunciation, end=" > ")
	print(vocab.word)
	if etymology:
		print(vocab.etymology)
		return
	print(vocab.chinese)
	print(vocab.english.replace("	", "\n"))
def record(vocab, delay=250, read=True):
	if vocab.desc == "":
		chinese = vocab.chinese
	else:
		chinese = vocab.desc
	wid = 0
	is_empty = True
	lines = vocab.english.split('\n')
	random.shuffle(lines)
	for line in lines:
		if len(line) < 2:
			continue
		if len(vocab.pronunciation) > 3:
			print(vocab.pronunciation, end=" > ")
			time.sleep(delay/4)
		print(vocab.word, end=" ")
		time.sleep(delay/4)
		print(line.replace("	", "\n"), end="\n\n")
		if read:
			Reader.english(vocab.word)
			Reader.english(line.replace("‘", "").replace("’", ""))
		is_empty = False
		break
	if is_empty:
		return
	logging.info(vocab.word)
	time.sleep(delay/4)
	print(vocab.chinese)
	time.sleep(delay/4)

def withdraw_all(ind=0, row=2): #>> {"word":cols}
	print(dirxlsm)
	workbook = xlrd.open_workbook(dirxlsm)
	sheet = workbook.sheet_by_index(ind)
	pool = []
	for rowx in range(sheet.nrows):
		if rowx < row:
			continue
		cols = sheet.row_values(rowx)
		w = cols[0] #A-item
		r = cols[1] #B-root
		i = cols[2] #C-index
		m = cols[3] #D-marking
		d = cols[4] #E-Description
		n = cols[5] #F-Note
		s = cols[6] #G-Synonym
		o = cols[7] #H-Order
		if len(w) < 1:
			continue
		if w[0] == '*':
			w = w[1:]
		pool.append(Vocab(w, r, m, i, d, n, s, o))
	return pool

def __opt(par):
	return par in sys.argv

def __read_par(par, ln=1):
	ind = sys.argv.index(par)
	arr = sys.argv[ind+1:ind+1+ln]
	return arr

def main():
	delay = 0
	start_index = 0
	order_index = 1000000

	if __opt("-silent"):
		Reader.silent = True
	if __opt("-delay"):
		delay = int(__read_par("-delay")[0])
	if __opt("-order"):
		order = int(__read_par("-order")[0])
	if __opt("-collec"):
		collec()
		return
	if __opt("-pn"):
		word = __read_par("-pn")[0]
		with open(Database.dirname+'/pronunciation.json', 'r') as f:
			pronunciation = json.load(f)
		if word in pronunciation:
			print(pronunciation[word])
		return
	if __opt("-p"):
		word = __read_par("-p")[0]
		p(Vocab(word))
		return

	if __opt("-o"):
		word = __read_par("-o")[0]
		p(Vocab(word), True)
		return
	if __opt("-r"):
		with open("word.log") as f:
			bank = []
			for ln in f.readlines():
				if len(ln) > 0:
					bank.append(ln.split("INFO:root:")[1].strip())
		pool = withdraw_all()
		size = len(pool)
		___a = []
		for vocab in pool:
			if not vocab.is_common:
				if vocab.ordr is None:
					continue
				# if vocab.ordr > order:
				# 	continue
				if vocab.mark == 1:
					continue
				if vocab.is_common:
					#p(vocab, 0, False)
					pass#continue
				if vocab.word not in bank:
					continue
				else:
					___a.append(vocab)
		random.shuffle(___a)
		for vocab in ___a:
			record(vocab, delay=delay, read=(not Reader.silent))	
		return	
	if __opt("-rand"):
		pool = withdraw_all()
		size = len(pool)
		___a = []
		for vocab in pool:
			if not vocab.is_common:
				if vocab.ordr is None:
					continue
				if vocab.ordr > order:
					continue
				if vocab.mark == 1:
					continue
				if vocab.is_common:
					#p(vocab, 0, False)
					pass#continue
				else:
					___a.append(vocab)
		random.shuffle(___a)
		for vocab in ___a:
			record(vocab, delay=delay, read=(not Reader.silent))
			raw_input()
		return
	pass

if __name__ == "__main__":
	main()