# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import Category
import xlrd

Category.dirname = os.path.dirname(Category.__file__)
dirxlsm = Category.dirname+"/Category.19.xlsm"

def withdraw_all(ind=0, row=2): #>> {"word":cols}
	print(dirxlsm)
	workbook = xlrd.open_workbook(dirxlsm)
	sheet = workbook.sheet_by_index(ind)
	pool = {}
	for rowx in range(sheet.nrows):
		if rowx < row:
			continue
		cols = sheet.row_values(rowx)
		i = cols[0] #A-index
		r = cols[1] #B-root
		w = cols[2] #C-item
		d = cols[3] #D-Description
		n = cols[4] #E-Note
		m = cols[5] #F-marking
		o = cols[6] #G-Order
		g = cols[7] #H-Orthography
		s = "" #G-Synonym
		if len(w) < 1:
			continue
		if w[0] == '*':
			w = w[1:]
		#Vocab(w, r, m, i, d, n, s, o)
		pool[w] = {"___o":o}
	return pool

def main():
	pool = withdraw_all()
	comp = []
	with open(Category.dirname+"/input.txt", "r") as f:
		for word in f.readlines():
			word = word.strip()
			if len(word) > 1:
				comp.append(word)
				if word in pool:
					print(word+"	"+str(pool[word]["___o"])[:-2])
				else:
					print(word+"	999999")


if __name__ == "__main__":
	main()