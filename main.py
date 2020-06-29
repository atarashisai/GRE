# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
import json
import pprint
import web
from Vocab import Vocab
import Reader
import time
import re

def __opt(par):
	return par in sys.argv

def __read_par(par, ln=1):
	ind = sys.argv.index(par)
	arr = sys.argv[ind+1:ind+1+ln]
	return arr

def write_to_backlog(word, data, log):
	if not log:
		return
	with open("backlog.txt", "a+") as f:
		f.write(word+"\n====\n")
		pprint.PrettyPrinter(indent=1, stream=f).pprint(data)
		f.write("****====\n")

def read_from_backlog():
	with open("backlog.txt", "r+") as f:
		array = []
		content = f.read()
		for x in content.split("****====\n"):
			print(x)
			if(len(x) < 2):
				continue
			word, correction = x.split("\n====\n")
			array.append((word, eval(correction)))
			#print(correction)
	web.L1.save_to_localfile_multiple(array)
		#	print_word(word, web.read(word), log=False)

def print_word(word, data, part=None, log=True):
	vocab = Vocab(word, data)
	if part != None:
		vocab.set_part(part)
	if vocab.exist: 
		vocab.pprint()
		write_to_backlog(vocab.word, data, log)
	else:
		return

def update(word):
	return web.update_from_local(word)
	#print_word(word, web.read(word))

def main():
	#data = L1.init()
	index = 0
	if __opt("-index"):
		index = int(__read_par("-index")[0])
	if __opt("-p"):
		word = __read_par("-p")[0]
		data = web.read(word)
		print_word(word, data)
		return
	if __opt("-update"):
		word = __read_par("-update")[0]
		data = web.update_from_web(word)
		vocab = Vocab(word, data)
		print_word(Vocab(word, data), data)
		return
	if __opt("-correct"):
		read_from_backlog()
		with open("backlog.txt", "w+") as f:
			pass
		return
	if __opt("-run"):
		while True:
			word = input(">")
			data = update(word)#web.read(word)
			print_word(word, data)
		return
	if __opt("-all"):
		i = 0
		# m = len(web.L1._data.keys())*1.0
		for word, data in web.L1._data.items():
			i+=1
			vocab = Vocab(word, data)
			if len(vocab.pronunciation) < 2:
				continue
			# if 'o' in word and 'au' in vocab.pronunciation and 'o' not in vocab.pronunciation and 'əw' not in vocab.pronunciation:
			# 	before = vocab.pronunciation
			# 	data = update(word)
			# 	#print(data)
			# 	vocab = Vocab(word, data)
			# 	after  = vocab.pronunciation
			# 	if before == after:
			# 		print("%.2f"%(i/m), word, vocab.pronunciation)
			# 		write_to_backlog(vocab.word, data, True)
			# 	continue
			# if 'r' in word and 'r' not in vocab.pronunciation:
			# 	before = vocab.pronunciation
			# 	data = update(word)
			# 	#print(data)
			# 	vocab = Vocab(word, data)
			# 	after  = vocab.pronunciation
			# 	if before == after:
			# 		print("%.2f"%(i/m), word, vocab.pronunciation)
			# 		write_to_backlog(vocab.word, data, True)
			# 	continue
			#print("%.2f"%(i/m), word, vocab.pronunciation, end="")
		return

	if __opt("-load"):
		filename = __read_par("-load")[0]
		with open(filename) as f:
			lines = f.readlines()
		for line in lines:
			if index > 0:
				index -= 1
				continue
			word, rank = line.strip().split("	")
			if len(rank) < 1:
				rank = 999999
			# if word.count(" ") > 0:
			# 	continue
			data = web.read(word)
			vocab = Vocab(word, data, rank=rank)
			vocab.pprint()
		return
	if __opt("-load-another"):
		from Vocab import printf
		filename = __read_par("-load-another")[0]
		with open(filename) as f:
			lines = f.readlines()
		for line in lines:
			if index > 0:
				index -= 1
				continue
			word, part, mean = line.strip().split("	")
			if word.count(" ") > 0:
				printf("*?? :: "+word)
			else:
				data = web.read(word)
				vocab = Vocab(word, data)
				vocab.set_part(part)
				vocab.pprint()
		return
	if __opt("-read"):
		filename = __read_par("-read")[0]
		with open(filename) as f:
			lines = f.readlines()
		for line in lines:
			if index > 0:
				index -= 1
				continue
			if len(line) < 3:
				continue
			#if line[0] != "*":
			#	continue
			#pair = line.strip().split(":: ")[1].split("　")
			#if len(pair) < 2:
			#	pair.append("")
			#phrase, chinese = pair
			phrase = line.strip().split("	")[0].lower()
			if phrase.count(" ") > 1:
				temp = phrase.split(" ")
				part = "adjective"
				word = temp[1]
			elif phrase.count(" ") > 0 and ',' in phrase:
				temp = phrase.split(", ")
				part = "adverb"
				word = temp[0]
			elif phrase.count(" ") > 0 and 'to ' in phrase:
				temp = phrase.split(" ")
				part = "verb"
				word = temp[1]
			elif phrase.count(" ") > 0 and 'be ' in phrase:
				temp = phrase.split(" ")
				part = "adjective"
				word = temp[1]
			elif phrase.count(" ") > 0 and 'the ' in phrase:
				temp = phrase.split(" ")
				part = "noun"
				word = temp[1]
			elif phrase.count(" ") > 0:
				temp = phrase.split(" ")
				part = 'noun'
				word = temp[1]
			else:
				part = ""
				word = phrase
			data = web.read(word)
			if __opt("-more"):
				print_word(word, data)
			else:
				vocab = Vocab(word, data)
				vocab.set_part(part)
				vocab.pprint(title_only=True)
			continue
			print(line)
			print_word(vocab, data, part=part)

			Reader.english(phrase)
			chinese = re.sub(r'（.*）', '', chinese)
			Reader.chinese(chinese)
			Reader.spell(",".join(list(word)))
			time.sleep(0.5)

if __name__ == "__main__":
	main()

if False:
	for each in data.keys():
		print_word(each, data[each])
		continue
		#print(data[each])

	L1.update_db()