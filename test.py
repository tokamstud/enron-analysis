line = '"guzman-m/all_documents/12.","Message-ID: <5255932.1075840580792.Javail.evans@thyme>'


start = line.find("Message-ID")+13
i=0
for char in line[start:]:
	i=i+1
	if (not (char.isdigit() or (char == '.'))):
		print(char)
		stop = i+start-2
		break

print(start)
print(stop)
print(line[start:stop])
