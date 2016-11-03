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
	def mapper_count(self, _, line):
		line = line.strip()
		point = len(line)
		if line.find('.","Message-ID: <') > 0:
			xfrom = line[1:line.find("/")]
			if len(xfrom) == 0:
				xfrom == "empty"
			yield xfrom, 1
	def combiner_count(self, key, values):
		yield key, sum(values)

	def reducer_count(self, key, values):
		yield key, sum(values)

	def mapper_cnt(self, key, values):
		yield 'Number of employees:::::', 1

	def reducer_cnt(self, key, values):
		yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
