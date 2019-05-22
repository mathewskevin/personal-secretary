#My_Tasks, My_Events
#function to sort file
#X XXXXXX XXXX
#X XXXXXX XXXXXX
#XXXXXXX XXXX XXXX
def sortFile(lookupFile):
        #get current contents of file
        fileObj = open(lookupFile) #readfile
        itemList = fileObj.readlines()
        fileObj.close()

        #sort current contents of file
        itemList.sort(key=lambda x:int(x.split()[2]))
        itemList.sort(key=lambda x:int(x.split()[1]))
        itemList.sort(key=lambda x:int(x.split()[0]))

        #paste sorted contents to file
        fileObjW = open(lookupFile,'w') #writefile

        for i in itemList:
                fileObjW.write(i)
        fileObjW.close()

#sort My_Schedule
def sortSpecial(lookupFile, option):
        #get current contents of file
        fileObj = open(lookupFile) #readfile
        itemList = fileObj.readlines()
        fileObj.close()

	if option == 0: #My_Schedule
        	#sort current contents of file
        	itemList.sort(key=lambda x:int(x.split()[2]))
        	itemList.sort(key=lambda x:int(x.split()[1]))
        	#itemList.sort(key=lambda x:int(x.split()[0]))
	if option == 1: #Special_Days
		itemList.sort(key=lambda x:int(x.split()[0]))
	else:
		itemList.sort(key=lambda x:int(x.split()[2]))
        	itemList.sort(key=lambda x:int(x.split()[1]))
        	itemList.sort(key=lambda x:int(x.split()[0]))

        #paste sorted contents to file
        fileObjW = open(lookupFile,'w') #writefile

        for i in itemList:
                fileObjW.write(i)
        fileObjW.close()