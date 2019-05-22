from __future__ import print_function
import datetime

def getCurrentDate():
	now = datetime.datetime.now()
	currentYear = now.year
	currentMonth = now.month
	myDay = str(now.day)
	myYear = str(currentYear)[2:]

	if currentMonth < 10:
		myMonth = '0' + str(currentMonth)
	else:
		myMonth = str(currentMonth)

	myDate = myYear + myMonth + myDay #generate current date in YYMMDD format
	return myDate

def getThreshDate(threshold):
	thresholdDate = datetime.date.today() + datetime.timedelta(days=threshold)
	threshYear = thresholdDate.year
	threshMonth = thresholdDate.month
	myYear = str(threshYear)[2:]
	threshDay = thresholdDate.day

	if threshMonth < 10:
		myMonth = '0' + str(threshMonth)
	else:
		myMonth = str(threshMonth)

	if threshDay < 10:
		myDay = '0' + str(threshDay)
	else:
		myDay = str(threshDay)

	myDate = myYear + myMonth + myDay #generate current date in YYMMDD format
	return myDate

#This code will convert a text time to a readable time
def timeConvert(timeText):
	hour = timeText[:2]
	minute = timeText[2:]

	time = str(hour) + ":" +  str(minute)
	return time

#This code wil convert a text date to a readable date
def dateConvert(dateText):
	#get numbers
	yearNum = dateText[:2]
	monthNum = dateText[2:4]
	dayText = dateText[4:]
	yearText = "20" + yearNum

	outputString = str(monthNum + "/" + dayText + "/" + yearNum)

	return outputString

def dateConvertMMMDD(dateText):
	#month dictionary
	monthList = {'01':'Jan',
		     '02':'Feb',
		     '03':'Mar',
		     '04':'Apr',
		     '05':'May',
		     '06':'Jun',
		     '07':'Jul',
		     '08':'Aug',
		     '09':'Sep',
		     '10':'Oct',
		     '11':'Nov',
                     '12':'Dec'}

	#get numbers
	yearNum = dateText[:2]
	monthNum = dateText[2:4]
	dayText = dateText[4:]
	yearText = "20" + yearNum

	if monthNum in monthList:
		monthText = monthList[monthNum]
		outputString = str(monthText + "-" + dayText)
	else:
		outputString = "???"

	return outputString

#This code wil convert a text date to a readable date
def dateConvertMMDD(dateText):
	#month dictionary
	monthList = {'01':'Jan',
		     '02':'Feb',
		     '03':'Mar',
		     '04':'Apr',
		     '05':'May',
		     '06':'Jun',
		     '07':'Jul',
		     '08':'Aug',
		     '09':'Sep',
		     '10':'Oct',
		     '11':'Nov',
                     '12':'Dec'}

	#get numbers
	monthNum = dateText[:2]
	dayText = dateText[2:]

	if monthNum in monthList:
		monthText = monthList[monthNum]
		outputString = str(monthText + "-" + dayText)
	else:
		outputString = "???"

	return outputString

def currentWeekDay():
	now = datetime.datetime.now()
	outputString = now.weekday()
	return outputString
#out = dateConvertMMDD("0617")
#print(out)
