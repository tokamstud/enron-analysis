from mrjob.job import MRJob


class MRCountSum(MRJob):

	def mapper(self, _, line):
		line = line.strip()
		if line.find("From:") == 0 and line.find("@enron.com") and (not (line.find("<"))) and (not (line.find("["))):
			login = line[line.find("From:")+5:line.find("@")].strip()
			if len(login) == 0:
				login == "empty"
			yield login, 1
	def combiner(self, key, values):
		yield key, sum(values)

	def reducer(self, key, values):
		yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
