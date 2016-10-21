from mrjob.job import MRJob


class MRCountSum(MRJob):

    def mapper(self, _, line):
        line = line.strip()  # remove leading and trailing whitespace
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        if line.find("Date:") == 0:
            for i, d in enumerate(days):
                week_day = line[line.find(d):line.find(d) + 3]
                if len(week_day) != 0:
                    week_day = str(i + 1) + ". " + week_day
                    break
            if len(week_day) == 0:
                week_day == "empty"
            yield week_day, 1

    def combiner(self, key, values):
        yield key, sum(values)

    def reducer(self, key, values):
        yield key, sum(values)


if __name__ == '__main__':
    MRCountSum.run()
