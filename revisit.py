# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import random
import time

def __opt(par):
	return par in sys.argv

def __read_par(par, ln=1):
	ind = sys.argv.index(par)
	arr = sys.argv[ind+1:ind+1+ln]
	return arr
def main():
	_delay_ = 0.5
	if __opt("-delay"):
		_delay_ = float(__read_par("-delay")[0])
	filename = __read_par("-load")[0]
	all_word = {}
	on = False
	with open(filename) as f:
		for ln in f:
			if ln[0] == "#":
				if ln[1] == "<":
					on = True
				if ln[1] == ">":
					on = False
				continue
			if not on:
				continue
			w = ln.split("  /")[0]
			all_word[w] = ln.split(">")
	all_word = all_word.values()
	print(len(all_word))
	while True:
		c = random.choice(all_word)
		i = random.randint(0, 1)
		print()
		print(c[i].strip())
		time.sleep(_delay_)
		print(c[i^1].strip())
	return
if __name__ == "__main__":
	main()