import L1json
from Tkinter import *
from ScrolledText import ScrolledText

def __edit(vocab):
	def __edit_ok():
		__cn = cn.get(1.0,END)
		__en = en.get(1.0,END)
		data["__cn"] = __cn
		data["__en"] = __en
		L1json.save_to_localfile(vocab.word, data)
		root.destroy()
	root = Tk()
	root.title(vocab.word)

	b = Button(root, text="OK", command=__edit_ok)
	b.pack()
	data = L1json.read(vocab.word)

	cn = ScrolledText(root)
	cn.pack()
	cn.insert(INSERT, data["__cn"])
	en = ScrolledText(root)
	en.pack()
	en.insert(INSERT, data["__en"])

	root.mainloop()