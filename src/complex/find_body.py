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
			MRStep(mapper=self.mapper_child,
				reducer=self.reducer_child),
			#MRStep(mapper_init=self.mapper_init_stat,
			#	mapper=self.mapper_stat)
			#MRStep(mapper=self.mapper_count_importance,
			#	reducer=self.reducer_count_importance),
			#MRStep(mapper=self.mapper_word,
			#	reducer=self.reducer_word),
			#MRSep(mapper=self.mapper_tree_nodes,
			#	reducer=self.reducer_tree_nodes)
			#MRStep(mapper=self.mapper_child_2, # count parents distinct
			#	reducer=self.reducer_child_2)
			]
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

# finds who has started most conversations11
#	def reducer_child(self, key, values):
#		relation = key[1]
#		from_mail = values[1][1]
#
#		if relation.find("parent") > -1:
#			yield key,1
#
#	def mapper_child_2(self, mail, relation):
#		yield mail, 1
#	def reducer_child_2(self, mail, values):
#		yield mail, sum(values)

# 	finds who has been in most conversations
	def reducer_child(self, key, values):
		lista = []

		#for mid in values:
		#	lista.append(mid)

		from_who = []
		for val in values:
			if not val[1][1] in from_who:
				from_who.append(val[1][1])
		num = len(from_who)
		#lista.append(num)
		if num > 50:
			yield key[0], num


# standard
	def reducer_child(self, key, values):
		lista = []

		for mid in values:
			lista.append(mid)

		from_who = []
		for val in values:
			if not val[1][1] in from_who:
				from_who.append(val[1][1])
		num = len(from_who)

		yield key[0], (key[0], lista)

# STEP 3 number of messages in thread++
	def mapper_init_stat(self):
		self.subject = ''
		self.value = {}
		self.start = False

	def mapper_stat(self, key, value):
		if key == self.subject:
			self.start = True
			if value[0] == "parent":
				self.value[value[0]] = value[1]
			elif value[0] == "child":
				self.value[value[0]] = value[1]
		else:
			if self.start:
				yield self.subject, self.value
				self.start = False
			else:
				self.subject = key
				self.start = False
				if value[0] == "parent":
					self.value[value[0]] = value[1]
				elif value[0] == "child":
					self.value[value[0]] = value[1]
# STEP 4 who was most active
	def mapper_count_importance(self, subject, data):
		for d in data:
			for s in data[d]:
				for i in [s]:
					yield i[1][1],1

	def reducer_count_importance(self, email, k):
		suma = sum(k)
		if suma > 150:
			yield int(suma),email

# STEP 4.1 <word> usage by date
	def mapper_word(self, subject, data):
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		years = ["1998", "1999", "2000", "2001", "2002"]
		monthn = 0
		year = ''
		for d in data:
			for s in data[d]:
				for i in [s]:
					# TODO: find "fraud"
					body = i[1][3]
					if "fraud" in body.lower():
						date = i[1][0]
						for m, month in enumerate(months):
							if month in date:
								monthn = m+1
						for y in years:
							if y in date:
								year = y
						yield (year, monthn), 1

	def reducer_word(self, date, k):
		yield date, sum(k)

if __name__ == '__main__':
	MRMultilineInput.run()
