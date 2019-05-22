from getTime import getCurrentDate, getThreshDate, timeConvert, dateConvert, dateConvertMMDD, dateConvertMMMDD, currentWeekDay 
import re

#Function to print tasks file
def readTasks(lookupFile):
	myDate = getThreshDate(0)
	threshDate = getThreshDate(7) #get tomorrow date
	reDate = re.compile(r'\d\d\d\d\d\d') #Regex for date
	fileObj = open(lookupFile)
	itemList = fileObj.readlines()
	fileObj.close()

	itemStrings = []

	#current Tasks
	for i in itemList:
	        mo1 = reDate.findall(i)

		#pull out parts of string
	        realAssignment = i[16:-1]
	        realStart = dateConvertMMMDD(mo1[0])
	        realEnd = dateConvertMMMDD(mo1[1])
	        completeFlag = i[0]
		
		#calculate Flag
		if myDate > mo1[1]: #late 'LATE'
			statusFlag = 1 #"LATE"
		elif threshDate >=  mo1[0] > myDate: #upcoming
			statusFlag = 4 #"Soon" 
		elif myDate == mo1[1]: #today '!!! '
			statusFlag = 2 #"!!!!"
		elif mo1[0] <= myDate < mo1[1]:
			statusFlag = 3 #"Cur."
		else:
			statusFlag = 5 #"...."

		if completeFlag == '1' and (mo1[0] <= threshDate):
			outputString = str(statusFlag) + " " + mo1[0] + " " + mo1[1] + " " + realStart + " " + realEnd + " " + realAssignment                        
			itemStrings.append(outputString)		
	       	else:
	                continue

	itemStrings.sort(key=lambda x:(x.split()[2]))
	itemStrings.sort(key=lambda x:(x.split()[1]))
	itemStrings.sort(key=lambda x:(x.split()[0]))
	newStrings = []

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
		len1 = len(newStrings[0][3])
		len2 = len(newStrings[0][4])
		#len3 = len(newStrings[1][5])

		b = ["Flag:","Start:","Due:","Task:"]
		print(b[0].ljust(7,' ') + b[1].ljust((len1 + spaceVal),' ') + b[2].ljust((len2 + spaceVal), ' ') + b[3].ljust(10, ' ')) #print col titles

		for i in newStrings:
			fullString = ' '.join(i)
			statusFlag = i[0]
			startDate = i[3]
			endDate = i[4]
			assignmentVal = fullString[(7 + 6 + 6 + len1 + len2 + 2):]	
			outputString = statusFlag.ljust(7,' ') + startDate.ljust((len1 + spaceVal),' ') + endDate.ljust((len2 + spaceVal),' ') + assignmentVal.ljust(10,' ')
			print(outputString)
	except IndexError:
		print('none')

#Function to print events file
def readEvents(lookupFile):
	myDate = getThreshDate(0)
	threshDate = getThreshDate(60) #get tomorrow date
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
		realEvent = i[14:-1]
		realDate = dateConvertMMMDD(mo1[0])
		realTime = timeConvert(i[9:13])
		completeFlag = i[0]
		
		#calculate Flag
		if myDate > mo1[0]: #late 'LATE'
			statusFlag = 1 #"LATE"
		elif threshDate >=  mo1[0] > myDate: #upcoming
			statusFlag = 4 #"Soon" 
		elif myDate == mo1[0]: #today '!!! '
			statusFlag = 2 #"!!!!"
		else:
			statusFlag = 3 #"...."

		if completeFlag == '1' and (mo1[0] <= threshDate):
			outputString = str(statusFlag) + " " + mo1[0] + " " +  realDate + " " + realTime + " " + realEvent                        
			#outputString = str(statusFlag) + " " + mo1[0] + " " + mo1[1] + " " + realStart + " " + realEnd + " " + realAssignment
			itemStrings.append(outputString)		
	       	else:
	                continue

	#itemStrings.sort(key=lambda x:(x.split()[2]))
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
		len1 = len(newStrings[0][2])
		len2 = len(newStrings[0][3])
		#len3 = len(newStrings[1][5])

		b = ["Flag:","Date:","Time:","Event/Place:"]
		print(b[0].ljust(7,' ') + b[1].ljust((len1 + spaceVal),' ') + b[2].ljust((len2 + spaceVal), ' ') + b[3].ljust(10, ' ')) #print col titles

		for i in newStrings:
			fullString = ' '.join(i)
			statusFlag = i[0]
			realDate = i[2]
			realTime = i[3]
			eventVal = fullString[(7 + 6 + len1 + len2 + 1):]	
			outputString = statusFlag.ljust(7,' ') + realDate.ljust((len1 + spaceVal),' ') + realTime.ljust((len2 + spaceVal),' ') + eventVal.ljust(10,' ')
			print(outputString)
	except IndexError:
		print('none')

#Function to print events file
def readSpecialDays(lookupFile, mode):
	startDate = getThreshDate(-10)[2:]
	myDate = getThreshDate(0)[2:]
	threshDate = getThreshDate(50)[2:] #get tomorrow date
	tomDate = getThreshDate(1)[2:]
	reDate = re.compile(r'\d\d\d\d\d\d') #Regex for date
	fileObj = open(lookupFile)
	itemList = fileObj.readlines()
	fileObj.close()

	itemStrings = []

	#current Tasks
	for i in itemList:
	        #mo1 = reDate.findall(i)

		#pull out parts of string
		realEvent = i[7:-1]
		realEventType = i[5:6]
		realDate = dateConvertMMDD(i[:4])
		
		#calculate Flag
		if threshDate >=  i[:4] > tomDate: #upcoming
			statusFlag = 4 #"Soon" 
		elif myDate == i[:4]: #today '!!! '
			statusFlag = 2 #"!!!!"
		elif tomDate == i[:4]: 
			statusFlag = 1 #Tom.
		else:
			statusFlag = 3 #"...."

		#Build sub-array #TO FIX
		if (startDate <= i[:4] <= threshDate): #if in this month
			outputString = str(statusFlag) + " " + realEventType + " " + i[:4] + " " + realDate + " " + realEvent                        
			#outputString = str(statusFlag) + " " + mo1[0] + " " + mo1[1] + " " + realStart + " " + realEnd + " " + realAssignment
			itemStrings.append(outputString)		
	       	else:
	                continue

	itemStrings.sort(key=lambda x:(x.split()[2]))
	itemStrings.sort(key=lambda x:(x.split()[1]))
	#itemStrings.sort(key=lambda x:(x.split()[0]))
	newStrings = []
	#pprint(itemStrings)


	for i in itemStrings:
		#print(i.split())
		newStrings.append(i.split())

	for i in newStrings:
		flag = i[0]
		if flag  == '1':
			i[0] = "Tom."
		elif flag  == '2':
			i[0] = " !! "
		elif flag == '3':
			i[0] = "past"
		elif flag == '4':
			i[0] = "    "
		else:
			i[0] = "????"

	try:
		#calculate col widths
		spaceVal = 2
		#len1 = len(newStrings[0][2])
		len2 = len(newStrings[0][3])
		#len3 = len(newStrings[1][5])

		bList = ["Flag:","Date:", "Birthday:"]
		print(bList[0].ljust(7,' ') + bList[1].ljust((len2 + spaceVal),' ') + bList[2].ljust(10, ' ')) #print col titles

		for i in newStrings:
			fullString = ' '.join(i)
			statusFlag = i[0]
			dayFlag = i[1]
			realDate = i[3]
			eventVal = fullString[19:]
			if dayFlag == mode:	
				outputString = statusFlag.ljust(7,' ') + realDate.ljust((len2 + spaceVal),' ') + eventVal.ljust(10,' ')
				print(outputString)
			else:
				continue
	
	except IndexError:
		print('none')			

#Function to print events file
def readSchedule(lookupFile):
	myDate = getThreshDate(0)
	tomDate = getThreshDate(1)
	daysWeekList = [5,6,0,1,2,3,4]
	todayWeekNum = currentWeekDay()

	if (todayWeekNum + 1) > 6:
		tomWeekNum = 0
	else:
		tomWeekNum = todayWeekNum + 1

	indexToday = daysWeekList.index(todayWeekNum)
	indexTom = daysWeekList.index(tomWeekNum)

	fileObj = open(lookupFile)
	itemList = fileObj.readlines()
	fileObj.close()

	itemStrings = []
	spaceFlag = 0

	#current Tasks
	for i in range(len(itemList)):
	        #mo1 = reDate.findall(i)
		
		#pull out parts of string
		todayText = itemList[i][0:7][indexToday]
		tomText = itemList[i][0:7][indexTom]
		timeStart = itemList[i][8:12]
		timeEnd = itemList[i][13:17]
		realEvent = itemList[i][18:-1]

		#calculate Flag
		if todayText == '1': #today
			statusFlag = 1
			dateFormat = dateConvertMMMDD(myDate)
		elif tomText == '1' and spaceFlag == 0:
			spaceFlag = 1
			statusFlag = 2 #"!!!!"
			i = i - 1
		elif tomText == '1' and spaceFlag == 1: #tomorrow
			statusFlag = 3 #"!!!!"
			dateFormat = dateConvertMMMDD(tomDate)
		else:
			statusFlag = 4 #"...." don't care

		#Build sub-array #TO FIX
		if (statusFlag == 1 or statusFlag == 3): #if today or tomorrow
			outputString = str(statusFlag) + " " + str(timeStart) + " " + dateFormat + " " + timeConvert(timeStart) + " " + timeConvert(timeEnd) + " " + realEvent                        
			#outputString = str(statusFlag) + " " + mo1[0] + " " + mo1[1] + " " + realStart + " " + realEnd + " " + realAssignment
			itemStrings.append(outputString)
		elif statusFlag == 2:
			outputString = str(statusFlag) + " " + "----" + " " + "----" + " " + "----" + " " + "----" + " " + "--------"
			itemStrings.append(outputString)
	       	else:
	                continue

	#itemStrings.sort(key=lambda x:(x.split()[2]))
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
			i[0] = "Tod."
		elif flag  == '2':
			i[0] = "Tom."
		elif flag  == '3':
			i[0] = "Tom."
		else:
			i[0] = "????"

	try:
		#calculate col widths
		spaceVal = 2
		len1 = len(newStrings[0][2])
		len2 = len(newStrings[0][3])
		#len3 = len(newStrings[1][5])

		bList = ["Date:", "Start:", "End:", "Event"]
		print(bList[0].ljust(8,' ') + bList[1].ljust((len1 + spaceVal),' ') + bList[2].ljust((len2 + spaceVal),' ') + bList[3].ljust(10, ' ')) #print col titles

		for i in newStrings:
			fullString = ' '.join(i)
			realDate = i[2]
			realStart = i[3]
			realEnd = i[4]
			eventVal = fullString[29:]	
			outputString = realDate.ljust(8,' ') + realStart.ljust((len1 + spaceVal),' ') + realEnd.ljust((len2 + spaceVal),' ') + eventVal.ljust(10,' ')
			print(outputString)
	except IndexError:
		print('none')

def printScheduleDay(indexPass, text):

	fileObj = open(text)
	itemList = fileObj.readlines()
	fileObj.close()

	itemStrings = []
	spaceFlags = [0,0,0,0,0,0,0]

	#[6,7,1,2,3,4,5]
	#current Tasks
	#indexPass = 1 #Saturday

	for i in range(len(itemList)):
	        #mo1 = reDate.findall(i)

		#pull out parts of string
		#pull out 0 or 1 for each day
		#tomText = itemList[i][0:7][indexTom]
		weekText = itemList[i][0:7]
		weekList = list(weekText)
		dayText = itemList[i][0:7][indexPass]
		timeStart = itemList[i][8:12]
		timeEnd = itemList[i][13:17]
		realEvent = itemList[i][18:-1]

		if dayText == '1':
			outputString = dayText + " " + str(timeStart) + " " + timeConvert(timeStart) + " " + timeConvert(timeEnd) + " " + realEvent
			itemStrings.append(outputString)
		else:
			continue

	itemStrings.sort(key=lambda x:(x.split()[1]))

	try:
		#calculate col widths
		spaceVal = 2

		b = ["Start:","End:","Event:"]
		print(b[0].ljust((5 + spaceVal),' ') + b[1].ljust((5 + spaceVal), ' ') + b[2].ljust(10, ' ')) #print col titles

		for i in itemStrings:
			startTime = i[7:12]
			endTime = i[13:18]
			eventVal = i[19:]	
			outputString = startTime.ljust((5 + spaceVal),' ') + endTime.ljust((5 + spaceVal),' ') + eventVal.ljust(10,' ')
			print(outputString)
	except IndexError:
		print('none')

def readSchedule2(text):
	print('Sunday:')
	printScheduleDay(0, text)
	print('\nMonday:')
	printScheduleDay(1, text)
	print('\nTuesday:')
	printScheduleDay(2, text)
	print('\nWednesday:')
	printScheduleDay(3, text)
	print('\nThursday:')
	printScheduleDay(4, text)
	print('\nFriday:')
	printScheduleDay(5, text)
	print('\nSaturday:')
	printScheduleDay(6, text)

#text = 'Special_Days.txt'
#readSpecialDays(text)
#text = 'My_Tasks.txt'
#readTasks(text) 
#text = 'My_Schedule.txt'
#0412 B Birthday 28 | Notes 28
#readSchedule(text)
#text = 'My_Events.txt'
#readEvents(text)
