from getTime import getCurrentDate, getThreshDate, timeConvert, dateConvert 
import re, os

'''
#Function to print Homework, Reading, &  Exams file
def readSchool(lookupFile):
	myDate = getCurrentDate()
	reDate = re.compile(r'\d\d\d\d\d\d') #Regex for date
	fileObj = open(lookupFile)
	itemList = fileObj.readlines()
	fileObj.close()

	b = ["Start:","Time:","Class:", "Assignment:"]
	print('\n' + b[0].ljust(8,' ') + b[1].ljust(8, ' ') + b[2]) #print col titles

	for i in itemList:
		mo1 = reDate.findall(i)

		realEvent = i[14:-1]
		realDate = dateConvert(mo1[0])
		realTime = timeConvert(i[9:13])
		completeFlag = i[0]
		itemStrings = [realDate, realTime, realEvent]

                if statusFlag == '1' and (mo1[0] == myDate):
                        print(realDate.ljust(8,' ') + realTime.ljust(8,' ') + realEvent.ljust(8,' '))
                else:
                        continue
'''

def readSchool(lookupFile):
	myDate = getThreshDate(0)
	threshDate = getThreshDate(7) #get tomorrow date
	tomDate = getThreshDate(1)
	reDate = re.compile(r'\d\d\d\d\d\d') #Regex for date
	fileObj = open(lookupFile)
	itemList = fileObj.readlines()
	fileObj.close()

	itemStrings = []

	#current Tasks
	for i in itemList:
	        mo1 = reDate.findall(i)

		#pull out parts of string
		completeFlag = i.split()[0]
		classText = i.split()[3]
		realStart = dateConvert(mo1[0])
		realEnd = dateConvert(mo1[1])
		completeFlag = i[0]
		realAssignment = i[(13 + 4 + len(classText)):-1]
		
		#calculate Flag
		if myDate > mo1[1]: #late 'LATE'
			statusFlag = 1 #"LATE"
		elif threshDate >=  mo1[0] > myDate: #upcoming
			statusFlag = 4 #"Soon" 
		elif myDate == mo1[1]: #today '!!! '
			statusFlag = 2 #"!!!!"
		else:
			statusFlag = 3 #"...."

		if completeFlag == '1' and (mo1[0] <= threshDate):
			outputString = str(statusFlag) + " " + mo1[0] + " " +  mo1[1] + " " + realStart + " " + realEnd + " " + classText + " " + realAssignment                       
			itemStrings.append(outputString)		
	       	else:
	                continue

	itemStrings.sort(key=lambda x:(x.split()[2]))
	itemStrings.sort(key=lambda x:(x.split()[1]))
	itemStrings.sort(key=lambda x:(x.split()[0]))
	newStrings = []
	#pprint(itemStrings)

	for i in itemStrings:
		#print(i.split())
		newStrings.append(i.split())

	for i in newStrings:
		flag = i[0]
		if flag  == '1':
			i[0] = "LATE"
		elif flag  == '2':
			i[0] = " !! "
		elif flag == '3':
			i[0] = "    "
		elif flag == '4':
			i[0] = "Soon"
		else:
			i[0] = "????"

	try:
		#calculate col widths
		spaceVal = 2
		len1 = len(newStrings[0][1])
		len2 = len(newStrings[0][2])
		len3 = len(newStrings[0][3])
		len4 = len(newStrings[0][4])
		len5 = len(newStrings[0][5])
		#len3 = len(newStrings[1][5])
		#print(len1, len2, len3)
		#print(newStrings[0][3], newStrings[0][4], newStrings[0][5])
		#print(' '.join(newStrings[0]))

		b = ["Flag:","Start:","Due:","Class:", "Assignment:"]
		print(b[0].ljust(7,' ') + b[1].ljust((len3 + spaceVal),' ') + b[2].ljust((len4 + spaceVal), ' ') + b[3].ljust(len5 + spaceVal, ' ') + b[4].ljust(10, ' ')) #print col titles

		for i in newStrings:
			fullString = ' '.join(i)
			statusFlag = i[0]
			realStart = i[3]
			realEnd = i[4]
			realClass = i[5]
			assignmentVal = fullString[(9 + len1 + len2 + len3 + len4 + len5 + 1):]
			outputString = statusFlag.ljust(7,' ') + realStart.ljust((len3 + spaceVal),' ') + realEnd.ljust((len4 + spaceVal),' ') + realClass.ljust((len5 + spaceVal),' ')  + assignmentVal.ljust(10,' ')
			#outputString = statusFlag.ljust(7,' ') + realDate.ljust((len1 + spaceVal),' ') + realTime.ljust((len2 + spaceVal),' ') + eventVal.ljust(10,' ')
			print(outputString)
	except IndexError:
		print('none')

#text_path = os.path.abspath('.')
#my_text = 'School_Reading.txt'
#readSchool(my_text)

