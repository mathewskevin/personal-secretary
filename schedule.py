#Kevin Mathews 08/22/2018 19:49
from __future__ import print_function
from sortFile import sortFile, sortSpecial
from readFile import readTasks, readEvents, readSpecialDays, readSchedule, readSchedule2
from readSchool import readSchool
from subprocess import call
import sys, datetime, os

EDITOR = os.environ.get('EDITOR','vim') #use vim for updating

#get today's date for comparison
#https://www.saltycrane.com/blog/2008/06/how-to-get-current-date-and-time-in/
now = datetime.datetime.now()

folderName = '/home/kmathews/Notes/Schedule/'
taskFile = folderName + 'My_Tasks.txt'
eventFile = folderName + 'My_Events.txt'
scheduleFile = folderName + 'My_Schedule.txt'
birthdayFile = folderName + 'Special_Days.txt'
homeworkFile = folderName + 'School_Homework.txt'
readingFile = folderName + 'School_Reading.txt'
examFile = folderName + 'School_Exams.txt'
separator = '---------------------------------------------------------'

def sortAll():
	sortFile(taskFile) #sort
	sortFile(eventFile) #sort
	sortFile(homeworkFile)
	sortFile(examFile)
	sortFile(readingFile)
	sortSpecial(birthdayFile, 1) #birthdays
	sortSpecial(scheduleFile, 0) #schedule

def printout():
	print('Last Update: ' + str(now) + '\n')
	print('Events:')
	readEvents(eventFile) #print contents
	print('\nHolidays:')
	readSpecialDays(birthdayFile, 'H')
	print('\nBirthdays:')
	readSpecialDays(birthdayFile, 'B')
	print('\nTasks:')
	readTasks(taskFile) #print contents
	print('\nExams:')
	readSchool(examFile)
	print('\nHomework:')
	readSchool(homeworkFile)
	print('\nReading:')
	readSchool(readingFile)
	print('\nWeekly Schedule:')
	readSchedule2(scheduleFile)

if len(sys.argv) < 2:
	print(separator)
	print('use "--help" for a full list of commands.')
	print(now)
    print('\nTasks:')
    readTasks(taskFile) #print contents
	print('\nAppointments:')
	readEvents(eventFile) #print contents
	print('\nHolidays:')
    readSpecialDays(birthdayFile, 'H')
	print('\nBe sure to check --birthdays')
	#print('\nTasks:')
	#readTasks(taskFile) #print contents
	#print('\nBirthdays:')
	#readSpecialDays(birthdayFile, 'B')
	print('')

elif len(sys.argv) > 3:
	print('use "--help" argument for proper usage.')

else:
	arg =  sys.argv[1]
	if arg == "--help":
		text1 = 'no arg     - print events & appointments.'
		text2 = '--sort      - sort items in all lists.'
		text3 = '--school    - print school items'
		text4 = '--week      - print weekly schedule'
		text5 = '--printout  - generate printout'
		text5 = '--birthdays - print holidays'
		text6 = '--write     - edit files'
		print(separator, '\n','Help:')
		print('\n',text1)
		print(text6) #write
		print(text2) #sort
		print(text3)
		#print(text4)
		print(text5,'\n')
	elif arg == "--sort": #UNIQUE OPTIONS
		sortAll()
		print(separator)
		print('\nitems sorted.\n')
	elif arg == "--week":
		#print('\n' + str(now))
		print(separator,'\n','Week:')
		print('\nAppointments:')
		#readEvents(eventFile)
		print('\n--------\nSchedule:\n--------')
		readSchedule2(scheduleFile)
		print('')
	elif arg == "--birthdays":
		print(separator, '\n', 'Holidays:')
		print('\nBirthdays:')
		readSpecialDays(birthdayFile, 'B')
		print('')
	elif arg == "--school":
	        print(separator, '\n', 'School:')
		print('\nExams:')
		readSchool(examFile)
		print('\nHomework:')
		readSchool(homeworkFile)
		print('\nReading:')
		readSchool(readingFile)
		print('')
	elif arg == "--printout":
	        print(separator,'\n','printout:')
		printout()
	elif arg == "--write":
		if len(sys.argv) == 3:
			choice = sys.argv[2]
			if choice == '0':
				pass
			elif choice == '1':
				call([EDITOR, taskFile]) #My_Tasks
			elif choice == '2':
				call([EDITOR, eventFile]) #My_Events
			elif choice == '3':
				call([EDITOR, scheduleFile]) #My_Schedule
			elif choice == '4':
				call([EDITOR, homeworkFile]) #School_Homework
			elif choice == '5':
				call([EDITOR, readingFile]) #School_Reading
			elif choice == '6':
				call([EDITOR, examFile]) #School_Exams
			elif choice == '7':
				call([EDITOR, birthdayFile]) #Special_Days
			else:
				print('error.')
		else:
			print(separator,'\n','write:')
			print('\nplease choose file to update:')
			text1 = ' 0. Cancel\n'
			text2 = '1. My Tasks\n'
			text3 = '2. My Events\n'
			text4 = '3. My Schedule\n'
			text5 = '4. School Homework\n'
			text6 = '5. School Reading\n'
			text7 = '6. School Exams\n'
			text8 = '7. Birthdays & Special Days\n'
			print(text1,text2,text3,text4,text5,text6,text7,text8)

	else:
		print('error: use "--help" argument for proper usage.')
