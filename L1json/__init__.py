import json
import shutil

where = None

_data = None
def init():
	global _data
	with open(where+"__data__.json", "r") as read_file:
		_data = json.load(read_file)

def save_to_localfile(word, content):
	global _data
	init()
	_data[word] = content
	shutil.copy(where+"__data__.json", where+"__data__.backup")
	with open(where+"__data__.json", 'w') as f:
		f.write(json.dumps(_data))

def read(word):
	return _data[word]

def found(word):
	return (word in _data)