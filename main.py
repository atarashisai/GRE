# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import time
from Vocab import Vocab
from Vocab import p
from Vocab import p_chinese
from Vocab import withdraw_all
from Vocab import withdraw_all_old
from Vocab import update
from Vocab import local_update
from Vocab import review
import Vocab as module_V
from random import randint
import random
module_V.dirname = os.path.dirname(module_V.__file__)

def __opt(par):
	return par in sys.argv

def __read_par(par, ln=1):
	ind = sys.argv.index(par)
	arr = sys.argv[ind+1:ind+1+ln]
	return arr

def __sort_method(vocab):
    return vocab.pronunciation

def main():
	__max__ = -1
	_delay_ = 0.5
	_index_ = -1
	_part__ = None
	if __opt("-max"):
		__max__ = int(__read_par("-max")[0])
	if __opt("-part"):
		_part__ = "("+__read_par("-part")[0].upper()+")"
	if __opt("-delay"):
		_delay_ = float(__read_par("-delay")[0])
	if __opt("-index"):
		_index_ = int(__read_par("-index")[0])
	if __opt("-review"):
		pool = withdraw_all(module_V.dirname+"/GRE.xlsx", review=True)
		while True:
			vocab = random.choice(pool)
			review(vocab, delay=_delay_)
		return
	if __opt("-edit"):
		word = __read_par("-edit")[0]
		from tool import __edit
		v = Vocab(word)
		__edit(v)
		p(v, delay=_delay_)
		return
	if __opt("-p"):
		word = __read_par("-p")[0]
		v = Vocab(word)
		p(v, delay=_delay_, part=_part__)
		return
	if __opt("-update"):
		word = __read_par("-update")[0]
		v = Vocab(word)
		update(v, delay=_delay_)
		return
	if __opt("-local-update"):
		word = __read_par("-local-update")[0]
		v = Vocab(word)
		update(v, delay=_delay_)
		return
	if __opt("-order"):
		#pool = withdraw_all(module_V.dirname+"/vocab.xlsx")
		pool = withdraw_all(module_V.dirname+"/GRE.xlsx")
		#pool.sort(key=__sort_method)
		for each in pool:
			try:
				if each.pronunciation == "":
					continue
				if each.checked == 1.0:
					continue
				p(each, delay=_delay_, part=_part__)
			except KeyError:
				local_update(each, delay=_delay_, part=_part__)
		return
	if __opt("-all"):
		#pool = withdraw_all(module_V.dirname+"/vocab.xlsx")
		pool = withdraw_all(module_V.dirname+"/GRE.xlsx")
		pool.sort(key=__sort_method)
		for each in pool:
			try:
				if each.pronunciation == "":
					continue
				p(each, delay=_delay_, part=_part__)
			except KeyError:
				local_update(each, delay=_delay_, part=_part__)
		return
	if __opt("-rand"):
		pool = withdraw_all(module_V.dirname+"/GRE.xlsx")
		pool.sort(key=__sort_method)
		if _index_ < 0:
			i = randint(0, len(pool))
		else:
			i = _index_
		for each in pool[i:]:
			try:
				if each.pronunciation == "":
					continue
				p(each, delay=_delay_, part=_part__)
			except KeyError:
				update(each, delay=_delay_, part=_part__)
			if __max__ > 0:
				__max__ -= 1
			if __max__ == 0:
				return
			#time.sleep(10)
		return
	if __opt("-ch"):
		word = __read_par("-ch")[0]
		print(Vocab(word).chinese)
		return
	if __opt("-old"):
		pool = withdraw_all_old(module_V.dirname+"/Category.19.xlsm")
		# n = len(pool)
		# i = 0
		# p1 = 0
		# p2 = 0
		# for each in pool:
		# 	Vocab(each).chinese
		# 	i += 1
		# 	p1 = i*100/n
		# 	if p1 > p2:
		# 		print("{}%".format(p1))
		# 		p2 = p1
		# return
		sorted_pool = []
		for each in pool:
			sorted_pool.append(Vocab(each))
		sorted_pool.sort(key=sort_method)

		for each in sorted_pool:
			p(each, skip=False, delay=_delay_)
			if __max__ > 0:
				__max__ -= 1
			if __max__ == 0:
				return
			#time.sleep(10)
		return
	# if __opt("-chinese-only"):
	# 	pool = withdraw_all(dirxlsm)
	# 	for each in pool:
	# 		p_chinese(Vocab(each), skip=False, delay=0)
	# 		if __max__ > 0:
	# 			__max__ -= 1
	# 		if __max__ == 0:
	# 			return
	# 		#time.sleep(10)
	# 	return
if __name__ == "__main__":
	main()