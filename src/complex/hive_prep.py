from mrjob.job import MRJob
from mrjob.step import MRStep

def get_id_from_line(line):
	if line.find('.","Message-ID: <') > 0:
		start = line.find("Message-ID")+13
		i=0
		for char in line[start:]:
			i=i+1
			if (not (char.isdigit() or (char == '.'))):
				stop = i+start-2
				break
		return line[start:stop]

class MRMultilineInput(MRJob):
	def steps(self):
		return [
			MRStep(mapper_init=self.mapper_init_count,
				mapper=self.mapper_count),
			MRStep(mapper=self.mapper_child)

# STEP 1
	def mapper_init_count(self):
		self.message_id = ''
		self.in_body = False
		self.body = []
		self.after_key = False
		self.beginning = False
		self.key = False

	def mapper_count(self, _, line):
		line = line.strip()

		if (line.find('.","Message-ID: <') > 0) and self.in_body and not self.beginning:
			yield self.message_id, self.body
			self.message_id = ''
			self.body = []
			self.in_body = False
			self.after_key = False
			self.beginning = False
			self.key = False

		if self.in_body and not self.after_key:
			self.beginning = False
			self.body.append(line)

		if line.find('.","Message-ID: <') > 0 and not self.key:
			if not self.in_body:
				self.in_body = True
				self.beginning = True
				self.after_key = True
				self.key = True
			start = line.find("Message-ID")+13
			i=0
			for char in line[start:]:
				i=i+1
				if (not (char.isdigit() or (char == '.'))):
					stop = i+start-2
					break
			self.message_id = line[start:stop]
		self.after_key = False

if __name__ == '__main__':
	MRMultilineInput.run()
