class FileHelper:
	def __init__(self, filename):
		self.filename = filename
		self.header = []
		self.body = []
		self.footer = []
		self.indent_level = 0

	def insert_header(self, content):
		""" Insert the Content in the Header section of the file. """
		self.header.append(content + "\n")

	def insert_content(self, content):
		""" Insert the Content in the Body section of the file. """
		self.body.append(("\t" * self.indent_level) + content + "\n")

	def insert_footer(self, content):
		""" Insert the Content in the Footer section of the file. """
		self.footer.append(content + "\n")

	def write_data_to_file(self):
		""" Write all the Data stored to File. """
		f = open(self.filename, 'w')
		f.writelines(self.header)
		f.writelines(self.body)
		f.writelines(self.footer)
		f.close()