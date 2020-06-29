# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3
if PY2:
	reload(sys)
	sys.setdefaultencoding('utf-8')
if PY3:
	import urllib.request as urllib
	def unicode(a,b):
		return a
	def encode(code, target):
		if isinstance(target, str):
			return target
		else:
			return str(target, encoding=code)
if PY2:
	import urllib
	def encode(code, target):

		return target.encode(code)

import lxml.html
from lxml.cssselect import CSSSelector
import os
import L1json
where = None

def __del_from_local(word):
	__save_to_localfile(word, "", ".html")

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

def __save_to_localfile(word, content, ext):
	with open(where+word+ext, 'w') as f:
		f.write(encode('utf-8', content))

def __download_english_html(word, save=True):
	link = "https://en.oxforddictionaries.com/definition/%s"%word
	content = __read_website(link)
	if content is None or not save:
		return None
	else:
		__save_to_localfile(word, content, ext=".html")
		return content

def __download_chinese_txt(word, save=True):
	x = ""
	link = "http://www.iciba.com/"+word
	selector = 'ul.base-list li'
	content = __read_website(link)
	if content is None:
		return ""
	tree = lxml.html.fromstring(content)
	for match in __select(tree, selector):
		x += match.text_content().replace(" ","").replace("\n","")+"\n"
	if save:
		__save_to_localfile(word, x, ext=".txt")
	return x

def __download_pronunciation_txt(word, save=True):
	x = ""
	if True:
		#Try website A
		link = "https://www.oxfordlearnersdictionaries.com/definition/english/"+word
		selector = 'div[geo$="n_am"] > span.phon'
		content = __read_website(link)
		if content is not None:
			ret = []
			tree = lxml.html.fromstring(content)
			for match in __select(tree, selector):
				ret.append(match.text_content()[1:-1])
			if len(ret) > 0:
				x = " | ".join(set(ret))

	if len(x) < 1:
		#Try website B if website A return an empty entry.
		selector = '.phoneticspelling'
		with open(where+word+".html", 'r') as f:
			content = f.read()
		if content is None:
			return ""
		ret = []
		tree = lxml.html.fromstring(content)
		for match in __select(tree, selector):
			ret.append(match.text_content()[1:-1])
		if len(ret) > 0:
			x = " | ".join(set(ret))
			x = x.replace("ʌɪ", "aɪ")
			x = x.replace("(", "")
			x = x.replace(")", "")
			x = x.replace("ɛ", "e")

	if save:
		__save_to_localfile(word, x, ext=".p")
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
		return __download_chinese_txt(word)
	return ""

def __get_pronunciation(word):
	if os.path.exists(where+word+".p"):
		with open(where+word+".p", 'r') as f:
			return f.read()
	else:
		return __download_pronunciation_txt(word)
	return ""

def __update_db(word, en, cn, pr, void=False):
	if void:
		ret = {"___v":3}
		ret["__pr"] = "*"
		ret["__en"] = ""
		ret["__cn"] = ""
		ret["__tg"] = ""
	else:
		ret = {"___v":3}
		ret["__pr"] = pr
		ret["__en"] = en
		ret["__cn"] = cn
		ret["__tg"] = ""
	if ret["__pr"] == "" and ret["__cn"] == "":
		__del_from_local(word)
		ret = {}
	else:
		ret = to_newformat(ret)
		L1json.save_to_localfile(word, ret)
	return ret

def to_newformat(ret):
	__pr = '1'
	__en = '2'
	__cn = '3'
	__tg = '4'
	new_format = {}
	new_format[__pr] = ret['__pr']
	new_format[__en] = {}
	meanings = ('\n'+ret['__en']).split('\n(')
	for meaning in meanings:
		if len(meaning) < 2:
			continue
		#print(meaning.rstrip().split("\t"))
		p,s,m,e = meaning.split("\t")
		p = p.replace(')', '')
		e = e.strip()
		if len(e) > 2 and e[0] == '‘' and e[-1] == '’':
			e = e[1:-1]
		if p not in new_format[__en]:
			new_format[__en][p] = []
		new_format[__en][p].append({
			'm':m,
			's':s,
			'e':e,
			'c':''
		})
	new_format[__cn] = {}
	chinese = ret['__cn'].split('\n')
	for chn in chinese:
		if len(chn) < 1:
			continue
		index = 0
		for letter in list(chn):
			if letter in list('asdfghjklzxcvbnmqwertyuiop.&'):
				index += 1
			else:
				break
		new_format[__cn][chn[0:index]] = chn[(index):]
	new_format[__tg] = ret['__tg']
	#pprint.PrettyPrinter(indent=1).pprint(new_format)
	#print(json.dumps(new_format, indent=4, sort_keys=True))
	#print(new_format)
	#print_word(each, new_format)
	#data[each] = new_format
	return new_format
'''
	private
	---------------------------
	public
'''

def read_from_web(word, save=True):
	#update English meaning from internet
	#update Chinese meaning from internet
	#update pronunciation from internet
	#save to local files
	en_content = __download_english_html(word, save)
	if en_content is None:
		return {}
	en = __get_english(en_content)
	cn = __download_chinese_txt(word, save)
	pr = __download_pronunciation_txt(word, save)

	return __update_db(word, en, cn, pr)

def read_from_local(word):
	if not os.path.exists(where+word+".html") or os.stat(where+word+".html").st_size < 1:
		return __update_db(word, None, None, "*", void=True)
	with open(where+word+".html", 'r') as f:
		en_content = f.read()
	en = __get_english(en_content)
	#cn = __get_chinese(word)

	cn = __download_chinese_txt(word)
	#pr = __get_pronunciation(word)
	pr = __download_pronunciation_txt(word, True)
	return __update_db(word, en, cn, pr)
