from mrjob.job import MRJob

class MRCountSum(MRJob):

	def mapper(self, _, line):
		line = line.strip()
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		years = ["1999", "2000", "2001"]

		if line.find("Date: ") == 0:
			point = len(line)
			if line.find("(PST)") == point-5:
				stop = 0
				found = False
				for month in months:
					if (month in line):
						stop = line.find(month)
						found = True
						break
				xfrom = line[stop:stop+8]
				if len(xfrom) == 0:
					xfrom == "empty"
				yield xfrom, 1
	def combiner(self, key, values):
		yield key, sum(values)

	def reducer(self, key, values):
		yield key, sum(values)
if __name__ == '__main__':
	MRCountSum.run()
