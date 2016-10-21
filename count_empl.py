from mrjob.job import MRJob


class MRCountSum(MRJob):

	def mapper(self, _, line):
		line = line.strip()
		if line.find("From:") == 0:
			if ("@enron" in line):
				login = line[line.find(" ")+1:line.find("@")]
			if len(login) == 0:
				login == "empty"
			yield login, 1
	def combiner(self, key, values):
		yield key, sum(values)

	def reducer(self, key, values):
		yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
