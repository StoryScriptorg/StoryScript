class FileHelper:
	def __init__(self, filename):
		self.filename = filename
		self.header = []
		self.body = []
		self.footer = []
		self.indentLevel = 0

	def insertHeader(self, content):
		""" Insert the Content in the Header section of the file. """
		self.header.append(content + "\n")

	def insertContent(self, content):
		""" Insert the Content in the Body section of the file. """
		self.body.append(("\t" * self.indentLevel) + content + "\n")

	def insertFooter(self, content):
		""" Insert the Content in the Footer section of the file. """
		self.footer.append(content + "\n")

	def writeDataToFile(self):
		""" Write all the Data stored to File. """
		f = open(self.filename, 'w')
		f.writelines(self.header)
		f.writelines(self.body)
		f.writelines(self.footer)
		f.close()