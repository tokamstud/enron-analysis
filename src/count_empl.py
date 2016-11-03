from mrjob.job import MRJob
from mrjob.step import MRStep


class MRCountSum(MRJob):
	def steps(self):
		return [
			MRStep(mapper=self.mapper_count,
				combiner=self.combiner_count,
				reducer=self.reducer_count),
			MRStep(mapper=self.mapper_cnt,
				reducer=self.reducer_cnt)
			]

	# STEP 1
	def mapper_count(self, _, line):
		line = line.strip()
		if line.find("From:") == 0 and line.find("@enron.com"):
			login = line[line.find("From:")+5:line.find("@enron")].strip()
			if len(login) == 0:
				login == "empty"
			yield login, 1
	def combiner_count(self, key, values):
		yield key, sum(values)

	def reducer_count(self, key, values):
		yield key, sum(values)

	# STEP 2
	def mapper_cnt(self, key, values):
		yield 'count', 1

	def reducer_cnt(self, key, values):
		yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
