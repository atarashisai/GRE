# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
	import urllib
	def encode(s, f):
		return s.encode(f)
if PY3:
	import urllib
	import urllib.request as urllib
	def unicode(s, f):
		return s
	def encode(s, f):
		return s.decode(f)
import lxml.html
from lxml.cssselect import CSSSelector
import os
import L1json
where = None

def __del_from_local(word):
	save_to_localfile(word, "")

def __read_website(link):
	for i in range(3):
		try:
			f = urllib.urlopen(link)
			content = unicode(f.read(), "utf-8")
			return content
		except IOError:
			continue
	return None

def __select(tree, selector):
	sel = CSSSelector(selector)
	results = sel(tree)
	return results

def __get_pronunciation(content):
	x = ""
	selector = '.phoneticspelling'
	ret = []
	tree = lxml.html.fromstring(content)
	for match in __select(tree, selector):
		ret.append(match.text_content()[1:-1])
	if len(ret) > 0:
		x = " | ".join(set(ret))
	return x

def __get_chinese_from_internet(word):
	x = ""
	link = "http://www.iciba.com/"+word
	selector = 'ul.base-list li'
	content = __read_website(link)
	if content is None:
		return ""
	tree = lxml.html.fromstring(content)
	for match in __select(tree, selector):
		x += match.text_content().replace(" ","").replace("\n","")+"\n"
	return x

def __get_english(content):
	x = ""
	selector = 'section.gramb'
	tree = lxml.html.fromstring(content)
	#sel = CSSSelector(selector)
	for match in __select(tree, selector):
		#results = sel(tree)
		ps = ""
		for pos in CSSSelector("span.pos")(match):
			ps = pos.text_content()
			break
		for m1 in CSSSelector("ul.semb li")(match):
			new_line = False
			title = "("+ps+")"
			label = ""
			for m2 in CSSSelector("span.sense-regions")(m1):
				label = m2.text_content().strip()
				break
			for m3 in CSSSelector("span.ind")(m1):
				new_line = True
				x += title+"	"+label+"	"+m3.text_content()+"	"
				break
			for m4 in CSSSelector("div.exg div.ex")(m1):
				if not new_line:
					x += title+"	"+label+"	"+"	"
				new_line = False
				x += " "+m4.text_content()+"\n"
				break
			if new_line:
				x += "\n"
	return x

def __get_chinese(word):
	if os.path.exists(where+word+".txt"):
		with open(where+word+".txt", 'r') as f:
			return f.read()
	else:
		ret = __get_chinese_from_internet(word)
		with open(where+word+".txt", 'w') as f:
			f.write(ret)
			return ret
	return ""

def __parse(word, content, void=False):
	if void:
		return {"__pr":"", "__en":"", "__cn":""}
	ret = {"___v":2}
	ret["__pr"] = __get_pronunciation(content)
	ret["__en"] = __get_english(content)
	ret["__cn"] = __get_chinese(word)
	if ret["__pr"] == "" and ret["__en"] == "":
		__del_from_local(word)
	else:
		L1json.save_to_localfile(word, ret)
	return ret

'''
	private
	---------------------------
	public
'''

def save_to_localfile(word, content):
	with open(where+word+".html", 'w') as f:
		f.write(encode(content,'utf-8'))

def read_from_web(word, save=True):
	link = "https://en.oxforddictionaries.com/definition/%s"%word
	content = __read_website(link)
	if content is None or not save:
		return {}
	else:
		save_to_localfile(word, content)
		return __parse(word, content)

def read_from_local(word):
	content = ""
	if os.stat(where+word+".html").st_size < 1:
		return __parse(None, None, void=True)
	with open(where+word+".html", 'r') as f:
		content = f.read()
	return __parse(word, content)
