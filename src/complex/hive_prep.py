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


# STEP 2
	def mapper_child(self, message_id, values):
		clean_body = ''
		clean_date = ''
		clean_from = ''
		clean_to = ''
		clean_values = []
		start = 0
		for idx, line in enumerate(values):
			if "Date:" in line:
				clean_date = line[5:].strip()
			if line.find("From:") == 0:
				clean_from = line[5:].strip()
			if line.find("To:") == 0:
				clean_to = line[3:].strip()
			if "X-FileName:" in line:
				start = idx+1
				break
		for i in range(start,len(values)):
			if "-Original Message-" in values[i]:
				break
			clean_body=clean_body + values[i] + " "

		clean_values.append(clean_date)
		clean_values.append(clean_from)
		#clean_values.append(clean_to)
		#clean_values.append(clean_body.strip())
		clean_values.append("TEST BODY")
		newval = values
		for element in values:
			if "subject:" in element.lower():
				subject = element
				break
		if "re:" in subject.lower():
			newval.append("child")
		elif "fw:" not in subject.lower():
			newval.append("parent")
		for element in newval:
			if "Subject:" in element:
				subject = element
				break
		relation = values[-1]
		i = 0
		colon = 0
		if "<" not in subject:
			for char in subject:
				i=i+1
				if char == ":":
					colon = i
			sub = subject[colon+1:].strip()
			sub_relation = []
			sub_relation.append(sub)
			sub_relation.append(relation)
			yield sub_relation, (message_id,clean_values)
if __name__ == '__main__':
	MRMultilineInput.run()
