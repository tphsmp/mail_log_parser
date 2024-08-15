import os
import re


#	directory with log files
directory = "/home/mrx/log/"
#	domain entry
entry = 'ivan.ivanov'

#	create list of archived logs
files = []
#	create list of .txt logs
filelog = []

#	getting order number of logfile
def extract_number(filename):
	return int(filename.split('.')[2])

#	pick only 'mail...log' files
for file in os.listdir(directory):
	if file.startswith('mail.') and file.endswith('.gz'):
		files.append(file)

#	extract .gz files in .txt files
for x in files:	
	command=os.system(f"zcat {directory}/{x} | grep {entry} -> {x}.txt")

#	make list of .txt logs
for file in os.listdir("/home/mrx"):
	if file.startswith('mail.log'):
		filelog.append(file)

#	sort .txt logs by order from greater one
sorted_log = sorted(filelog, key=extract_number, reverse=True)
#print(sorted_log)

#	merge all .txt logs in one
with open('log_.txt', 'w') as outfile:
	for f in sorted_log:
		with open(f, 'r') as infile:
			for line in infile:
				outfile.write(line)

#	create list of e-mail IDs
#	path to logfile
logfile = 'log_.txt'

#	path to .txt log
dir = '/home/mrx'

#	extract email IDs from log files
def extract_ids_from_logs(directory):
	result = []
	for filename in os.listdir(directory):
		if filename.startswith('mail.log') and filename.endswith('gz.txt'):
			file_path = os.path.join(directory, filename)
			try:
				with open(file_path, 'r') as file:
					for line in file:
						match = re.search(r'(\w{10}):', line)
						if match:
							id = match.group(1)
							result.append({filename[:-4]: id})
			except Exception as ex:
				print(ex)
	return result

#	create email ids list
ids_list = extract_ids_from_logs(dir)


#	creating .txt file of email logs by ids
for entry in ids_list:
	for x, id in entry.items():
		command = os.system(f"zcat {directory}/{x} | grep {id} -> id_{id}.txt")

#	merge id_log files in one
#       make list of email id logs
id_list = []

for file in os.listdir("/home/mrx"):
        if file.startswith('id_'):
                id_list.append(file)

#       merge all .txt logs in one
with open('log_by_email_id.txt', 'w') as outfile:
        for id in id_list:
                with open(id, 'r') as infile:
                        for line in infile:
                                outfile.write(line)

#	remove unpacked logs, leave merged .txts
os.system("rm id_*.txt")
os.system("rm mail.log*.txt")
