import tkinter as tk

# skipcq PYL-W0613
def pack(refType, refVal, **arguments):
	refVal.pack(**arguments)

# Module Info
TYPES: dict = {
	"TkWindow": {
		"methods": {
			"mainloop": lambda refType, refVal, arguments: refVal.mainloop(),
			"title": lambda refType, refVal, arguments: refVal.title(arguments[0])
		}
	},
	"TkLabel": {
		"methods": {
			"pack": pack
		}
	},
	"TkButton": {},
	"TkTextField": {}
}
STATIC_METHODS: dict = {
	"Tk": {"returntype": "TkWindow", "action": tk.Tk, "arguments": []},
	"Label": {
		"returntype": "TkLabel", 
		"action": tk.Label, 
		"arguments": [
			# argument 0 of type "TkWindow"
			"TkWindow", 
			# named argument 0 "text" of type "string"
			"text=string"
		]
	}
}

if __name__ == "__main__":
	# The code below will be the simulation that the following sample code do:
	# import tkinter as tk
	# TkWindow win = tk.Tk()
	# win.title("Hello, world!")
	# TkLabel label = new tk.Label(win, text="Hello, world!")
	# label.pack()
	# win.mainloop()
	win = {"type": STATIC_METHODS["Tk"]["returntype"], "value": STATIC_METHODS["Tk"]["action"]()}
	TYPES[win["type"]]["methods"]["title"](win["type"], win["value"], ["Hello, world!"])
	label = {"type": STATIC_METHODS["Label"]["returntype"], "value": STATIC_METHODS["Label"]["action"](win["value"], text="Hello, world!")}
	TYPES[label["type"]]["methods"]["pack"](label["type"], label["value"], **{})
	TYPES[win["type"]]["methods"]["mainloop"](win["type"], win["value"], [""])

