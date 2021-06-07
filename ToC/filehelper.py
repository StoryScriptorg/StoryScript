class FileHelper:
	def __init__(self, filename):
		self.filename = filename
		self.header = []
		self.body = []
		self.footer = []
		self.indentLevel = 0

	def insertHeader(self, content):
		self.header.append(content + "\n")

	def insertContent(self, content):
		self.body.append(("\t" * self.indentLevel) + content + "\n")

	def insertFooter(self, content):
		self.footer.append(content + "\n")

	def writeDataToFile(self):
		f = open(self.filename, 'w')
		f.writelines(self.header)
		f.writelines(self.body)
		f.writelines(self.footer)
		f.close()