import os
import L1json as L1
import L2html
import time

class Dictionary:
	def __init__(self, loc, ext):
		self.loc = loc+"\\"
		self.ext = ext
	def found(self, word):
		return os.path.exists(self.loc+word+self.ext) and os.stat(self.loc+word+self.ext).st_size > 1

L1.where = os.path.dirname(L1.__file__)+"\\"
L1.init()
L2 = Dictionary(os.path.dirname(L2html.__file__), ".html")
L2.read = L2html.read_from_local
L2.read_from_web = L2html.read_from_web
L2html.where = L2.loc

def update_from_web(word):
	L2.read_from_web(word)

def update_from_local(word):
	L2.read(word)
	
def get_pronunciation(word, L1only=False):
	if L1.found(word):
		__pr = L1.read(word)['__pr']
		return __pr
	if L1only:
		return ""
	if L2.found(word):
		__pr = L2.read(word)['__pr']
		return __pr
	__pr = L2.read_from_web(word)['__pr']
	return __pr

def get_english(word):
	if L1.found(word):
		__en = L1.read(word)['__en']
		return __en
	if L2.found(word):
		__en = L2.read(word)['__en']
		return __en
	__en = L2.read_from_web(word)['__en']
	return __en

def get_chinese(word):
	if L1.found(word):
		__cn = L1.read(word)['__cn']
		return __cn
	if L2.found(word):
		__cn = L2.read(word)['__cn']
		return __cn
	__cn = L2.read_from_web(word)['__cn']
	return __cn