from mrjob.job import MRJob


class MRCountSum(MRJob):

	def mapper(self, _, line):
		str += line
		i += 1
		if i == 5:
			i = 0
			yield str, len(str)

	#def combiner(self, key, values):
	#	yield key, sum(values)

	#def reducer(self, key, values):
	#	yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
