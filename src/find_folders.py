from mrjob.job import MRJob

class MRCountSum(MRJob):

	def mapper(self, _, line):
		line = line.strip()
		months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
		if line.find("X-Folder:") == 0:
			stop = 0
			found = False
			for month in months:
				if (month in line):
					stop = line.find(month)
					found = True
					break
			if (not found):
				stop = line.find("\\",13)
			for char in line[12:stop]:
				if char.isdigit():
					stop = line.find(char)
					break
			xfrom = line[line.find("X-Folder:"):stop]
			if len(xfrom) == 0:
				xfrom == "empty"
			yield xfrom, 1
	def combiner(self, key, values):
		yield key, sum(values)

	def reducer(self, key, values):
		yield key, sum(values)

if __name__ == '__main__':
	MRCountSum.run()
