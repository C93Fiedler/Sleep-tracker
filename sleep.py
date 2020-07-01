from __future__ import division
import pygame, sys, os
from pygame.locals import *
import random 
import threading
import copy

global gameon, threadnumber, allyears, currentyearpos

class BlitThread(threading.Thread):
    def __init__(self,ID):
        threading.Thread.__init__(self)
        self.ID=ID
        self.state=1
        self.showtimegridstatus=True
        #images
        self.menubackground=pygame.image.load(os.path.join(
            "data","menubackground.png")).convert()
        self.timegrid=pygame.image.load(os.path.join(
            "data","timegrid.png")).convert()
        self.timegrid.set_colorkey((255,255,255))
        self.displaytimegrid=pygame.image.load(os.path.join(
            "data","displaytimegrid.png")).convert()
        self.hidetimegrid=pygame.image.load(os.path.join(
            "data","hidetimegrid.png")).convert()
        self.wokemarker=pygame.image.load(os.path.join(
            "data","wokemarker.png")).convert()
        self.sleepmarker=pygame.image.load(os.path.join(
            "data","sleepmarker.png")).convert()
        self.unpressedmonths=pygame.image.load(os.path.join(
            "data","unpressedmonth.png")).convert()
        self.pressedmonth=pygame.image.load(os.path.join(
            "data","pressedmonth.png")).convert()
        self.monthnames=pygame.image.load(os.path.join(
            "data","monthnames.png")).convert()
        self.monthnames.set_colorkey((127,127,127))
        self.monthdayselected=pygame.image.load(os.path.join(
            "data","monthdayselected.png")).convert()
        self.emptyleftyeararrow=pygame.image.load(os.path.join(
            "data","emptyleftyeararrow.png")).convert()
        self.emptyrightyeararrow=pygame.image.load(os.path.join(
            "data","emptyrightyeararrow.png")).convert()
        self.leftyeararrow=pygame.image.load(os.path.join(
            "data","leftyeararrow.png")).convert()
        self.rightyeararrow=pygame.image.load(os.path.join(
            "data","rightyeararrow.png")).convert()
        #text
        self.daynumbertext=[]
        for x in range(1,32):
            self.daynumbertext.append(pygame.font.Font("freesansbold.ttf", 10).render(
                        str(x),
                        0,(0,0,0)))
        

        
    def run(self):
        global gameon, threadnumber, allyears, currentyearpos
        while gameon:
            clock.tick(20)
            screen.blit(self.menubackground, (0,0))
            #fill in the plot
            for x in range(0,31):#days
                for y in range(0,288):#intervals
                    if allyears[currentyearpos].date[allyears[currentyearpos].currentmonthtracked][x][y]==1:#sleep
                        screen.blit(self.sleepmarker, (40+18*x,308-y))
                    elif allyears[currentyearpos].date[allyears[currentyearpos].currentmonthtracked][x][y]==2:#woke
                        screen.blit(self.wokemarker, (40+18*x,308-y))
            #time grid


            if self.showtimegridstatus:
                screen.blit(self.hidetimegrid, (620,20))
                screen.blit(self.timegrid,(27,27))
            else:
                screen.blit(self.displaytimegrid, (620,20))

            #month selection
            #print allyears[currentyearpos].currentmonthtracked
            screen.blit(self.unpressedmonths, (620,120))
            screen.blit(self.pressedmonth, (620+44*int((allyears[currentyearpos].currentmonthtracked+3)%3),120+27*int(allyears[currentyearpos].currentmonthtracked/3)))
            screen.blit(self.monthnames, (620,120))
            #dates relating to days of the week
            counter=allyears[currentyearpos].firstday[allyears[currentyearpos].currentmonthtracked]
            counter2=0
            counter3=0#for tracking which day is selected
            for x in range(0,allyears[currentyearpos].monthlength[allyears[currentyearpos].currentmonthtracked]):
                if counter3==allyears[currentyearpos].currentdaytracked:
                    screen.blit(self.monthdayselected, (608+25*counter,267+15*counter2))
                counter3+=1
                screen.blit(self.daynumbertext[x], (615+25*counter,270+15*counter2))
                counter+=1
                if counter==7:
                    counter=0
                    counter2+=1
            #year selection
            screen.blit(pygame.font.Font("freesansbold.ttf", 20).render(
                        str(allyears[currentyearpos].yearnumber),
                        0,(0,0,0)),(660,95))
            if not currentyearpos:
                screen.blit(self.emptyleftyeararrow, (645,95))
            else:
                screen.blit(self.leftyeararrow, (645,95))
            if currentyearpos+1==len(allyears):
                screen.blit(self.emptyrightyeararrow, (715,95))
            else:
                screen.blit(self.rightyeararrow, (715,95))
            #averages
            screen.blit(pygame.font.Font("freesansbold.ttf", 20).render(
                        "Total day sleep time: " +str(allyears[currentyearpos].averagedsleepdate[allyears[currentyearpos].currentmonthtracked][allyears[currentyearpos].currentdaytracked]/12)+" hours",
                        0,(0,0,0)),(20,500))
            screen.blit(pygame.font.Font("freesansbold.ttf", 20).render(
                        "Total day awake time: " +str(allyears[currentyearpos].averagedwokedate[allyears[currentyearpos].currentmonthtracked][allyears[currentyearpos].currentdaytracked]/12)+" hours",
                        0,(0,0,0)),(20,525))
            screen.blit(pygame.font.Font("freesansbold.ttf", 20).render(
                        "Total month sleep time: " +str(allyears[currentyearpos].averagedsleepmonth[allyears[currentyearpos].currentmonthtracked]/12)+" hours",
                        0,(0,0,0)),(20,550))
            screen.blit(pygame.font.Font("freesansbold.ttf", 20).render(
                        "Total month awake time: " +str(allyears[currentyearpos].averagedwokemonth[allyears[currentyearpos].currentmonthtracked]/12)+" hours",
                        0,(0,0,0)),(20,575))
            pygame.display.flip()
        threadnumber-=1


class CalendarYear:
    def __init__(self, thisyearnumber):
        self.yearnumber=thisyearnumber
        #they all point to the same day #self.date=12*[31*[288*[0]]] #12 months,31 days, each has 288 5min intervals, 0 means no data
        self.averagedsleepdate=[] #average sleep per day to display
        self.averagedwokedate=[] #average woke per day to display
        self.averagedsleepmonth=[] #average sleep per month to display
        self.averagedwokemonth=[] #average woke per month to display
        day=288*[0]
        month=[]
        averagedmonth=[]
        self.date=[]
        for x in range(0,31):
            month.append(copy.deepcopy(day))
            averagedmonth.append([])
        for x in range(0,12):
            self.date.append(copy.deepcopy(month))
            self.averagedsleepdate.append(copy.deepcopy(averagedmonth))
            self.averagedwokedate.append(copy.deepcopy(averagedmonth))
        self.currentmonthtracked=0
        self.currentdaytracked=0
        self.monthlength=[31,28,31,30,31,30,31,31,30,31,30,31]
        #first day of the month: 0 - monday, 1 - tuesday, ...
        self.firstday=[]
        if thisyearnumber==2020:
            self.firstday.append(2)
        else:
            self.firstday.append(int((3+(thisyearnumber-2020)*365+int((thisyearnumber-2021)/4))%7))
        self.firstday.append(int((self.firstday[-1]+31)%7))
        if thisyearnumber%4:
            self.firstday.append(int((self.firstday[-1]+28)%7))
        else:
            self.firstday.append(int((self.firstday[-1]+29)%7))
            self.monthlength[1]=29
        self.firstday.append(int((self.firstday[-1]+31)%7))
        self.firstday.append(int((self.firstday[-1]+30)%7))
        self.firstday.append(int((self.firstday[-1]+31)%7))
        self.firstday.append(int((self.firstday[-1]+30)%7))
        self.firstday.append(int((self.firstday[-1]+31)%7))
        self.firstday.append(int((self.firstday[-1]+31)%7))
        self.firstday.append(int((self.firstday[-1]+30)%7))
        self.firstday.append(int((self.firstday[-1]+31)%7))
        self.firstday.append(int((self.firstday[-1]+30)%7))
        
    def CalculateAverages(self):
        #per day
        for month in range(0,len(self.date)):
            for day in range(0,len(self.date[month])):
                self.averagedsleepdate[month][day]=self.date[month][day].count(1)
                self.averagedwokedate[month][day]=self.date[month][day].count(2)
        #per month
        for month in range(0,len(self.averagedsleepdate)):
            totalsleepincrements=0
            for day in range(0,len(self.averagedsleepdate[month])):
                totalsleepincrements+=self.averagedsleepdate[month][day]
            self.averagedsleepmonth.append(totalsleepincrements)
        for month in range(0,len(self.averagedwokedate)):
            totalwokeincrements=0
            for day in range(0,len(self.averagedwokedate[month])):
                totalwokeincrements+=self.averagedwokedate[month][day]
            self.averagedwokemonth.append(totalwokeincrements)

def Loadsleepdata():
    thefile=open(os.path.join("data","sleep.txt"), "r")
    linedata=''
    timestamps=[] #list containing date and time of status change corresponding to statuses list
                  # in the form '01/01/2020 01:10'
    statuses=[] #list containing 'woke' and 'sleep'
    yearlist=[] #list of created years
    years=[] #store with CalendarYear
    for line in thefile:
        linedata=linedata+line
    linedata=linedata.split('\n') #linedata has each individual line
    thefile.close()
    for x in range(1,len(linedata)): #zeroth line has info
        linedata[x]=linedata[x].split(' ')
        if linedata[x][2]=='0':
            pass
        else:
            linedate=linedata[x][1][:-1].split('/')#[-1] to delete the ':', split into ['01', '01', '2020']
            if linedate[2] not in yearlist:
                yearlist.append(linedate[2])
                years.append(CalendarYear(int(linedate[2])))#create the year
            statusdata=linedata[x][2:]#cut off the date
            for y in range(0,int(len(statusdata)/3)):#int because it makes it float
                statuses.append(statusdata[y*3]) #sleep/woke
                timestamps.append(linedate[0]+'/'+linedate[1]+'/'+linedate[2]+' '+statusdata[2+y*3]) #date+time
    currentdatechange=timestamps[0].split(' ')[0].split('/')#date ['01', '01', '2020']
    currenttimestart=timestamps[0].split(' ')[1].split(':')#time ['13', '10']
    #print timestamps
    for x in range(1,len(statuses)):
        #print timestamps[x]
        nextdatechange=timestamps[x].split(' ')[0].split('/')#date
        nexttimestart=timestamps[x].split(' ')[1].split(':')
        for year in years:
            if year.yearnumber==int(currentdatechange[2]): #found the year corresponding to date
                #need to work out how many 5min intervals between status changes
                intervalsintofirstday=int(int(currenttimestart[0])*12+int(currenttimestart[1])/5) #time of first change
                if currentdatechange[0]==nextdatechange[0] and currentdatechange[1]==nextdatechange[1]:#same day change
                    totalintervals=int(int(nexttimestart[0])*12+int(nexttimestart[1])/5-intervalsintofirstday)#total number of intervals
                    for y in range(0,totalintervals):
                        if statuses[x-1]=='woke':
                            #print "woke"
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][intervalsintofirstday-1+y]=2
                        else:
                            #print "sleep"
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][intervalsintofirstday-1+y]=1
                elif currentdatechange[1]==nextdatechange[1]:#same month change
                    #first fill in the first day
                    for y in range(intervalsintofirstday-1,288):
                        if statuses[x-1]=='woke':
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=2
                        else:
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=1
                    #calculate how many days till next change:
                    dayschanged=int(nextdatechange[0])-int(currentdatechange[0])
                    #fill days changed if status didnt change for more than a day
                    for z in range(1,int(dayschanged)):
                        for y in range(0,288):
                            if statuses[x-1]=='woke':
                                year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1+z][y]=2
                            else:
                                year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1+z][y]=1
                    #how many intervals left in the last day
                    intervalsintolastday=int(nexttimestart[0])*12+int(nexttimestart[1])/5
                    #fill the last day
                    for y in range(0,int(intervalsintolastday)):
                        if statuses[x-1]=='woke':
                            year.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=2
                        else:
                            year.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=1
                elif currentdatechange[2]==nextdatechange[2]:#same year change
                    #first fill in the first day
                    #print currentdatechange
                    #print year.monthlength[int(currentdatechange[1])-1]
                    for y in range(intervalsintofirstday-1,288):
                        if statuses[x-1]=='woke':
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=2
                        else:
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=1
                    #fill the remaining days but need to ignore days that don't exist(eg 31 november)
                    if int(currentdatechange[0])!=year.monthlength[int(currentdatechange[1])-1]:
                        for y in range(int(currentdatechange[0]),year.monthlength[int(currentdatechange[1])-1]):
                            #print y
                            #print currentdatechange
                            for z in range(0,288):
                                if statuses[x-1]=='woke':
                                    year.date[int(currentdatechange[1])-1][y][z]=2
                                else:
                                    year.date[int(currentdatechange[1])-1][y][z]=1
                    #calculate how many days in the new month:
                    dayschanged=int(nextdatechange[0])
                    #fill days changed if status didnt change for more than a day
                    for z in range(1,int(dayschanged)):
                        for y in range(0,288):
                            if statuses[x-1]=='woke':
                                year.date[int(currentdatechange[1])][-1+z][y]=2
                            else:
                                year.date[int(currentdatechange[1])][-1+z][y]=1
                    #how many intervals left in the last day
                    intervalsintolastday=int(nexttimestart[0])*12+int(nexttimestart[1])/5
                    #fill the last day
                    for y in range(0,int(intervalsintolastday)):
                        if statuses[x-1]=='woke':
                            year.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=2
                        else:
                            year.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=1
                else: #new year
                    #first fill in the first day
                    for y in range(intervalsintofirstday-1,288):
                        if statuses[x-1]=='woke':
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=2
                        else:
                            year.date[int(currentdatechange[1])-1][int(currentdatechange[0])-1][y]=1
                    #fill the remaining days but need to ignore days that don't exist(eg 31 november), i mean it should be dec so shouldn't matter but just in case
                    if int(currentdatechange[0])!=year.monthlength[int(currentdatechange[1])-1]:
                        for y in range(int(currentdatechange[0]),year.monthlength[int(currentdatechange[1])-1]):
                            for z in range(0,288):
                                if statuses[x-1]=='woke':
                                    year.date[int(currentdatechange[1])-1][y][z]=2
                                else:
                                    year.date[int(currentdatechange[1])-1][y][z]=1
                    #fill the new year
                    for year2 in years:
                        if year2.yearnumber==int(nextdatechange[2]):
                            #fill all days that are with no change
                            for y in range(0, int(nextdatechange[0])-1):
                                for z in range(0,288):
                                    if statuses[x-1]=='woke':
                                        year2.date[int(nextdatechange[1])-1][y][z]=2
                                    else:
                                        year2.date[int(nextdatechange[1])-1][y][z]=1
                            #fill the final day
                            intervalsintolastday=int(nexttimestart[0])*12+int(nexttimestart[1])/5
                            for y in range(0,int(intervalsintolastday)):
                                if statuses[x-1]=='woke':
                                    year2.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=2
                                else:
                                    year2.date[int(nextdatechange[1])-1][int(nextdatechange[0])-1][y]=1
        currentdatechange=timestamps[x].split(' ')[0].split('/')#date ['01', '01', '2020']
        currenttimestart=timestamps[x].split(' ')[1].split(':')#time ['13', '10']
    return years


                             
gameon=True
threadnumber=1
pygame.init()
clock=pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('My sleep') 
rate=30

allyears=Loadsleepdata()
currentyearpos=0
#print allyears[currentyearpos].date[1][2]
for x in allyears:
    x.CalculateAverages()

blitthread=BlitThread(1)
blitthread.start()


while gameon:
    clock.tick(rate)
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        gameon=False
        while threadnumber:#wait for all threads to finish
            pass
        pygame.quit()
        sys.exit()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button==1:
            fcpos=pygame.mouse.get_pos()
            if 620<fcpos[0]<783 and 20<fcpos[1]<58: #show time grid
                if blitthread.showtimegridstatus:
                    blitthread.showtimegridstatus=False
                else:
                    blitthread.showtimegridstatus=True
            elif 620<fcpos[0]<752 and 120<fcpos[1]<228:#change month
                allyears[currentyearpos].currentmonthtracked=int(int((fcpos[0]-620)/44)%3)+int(int((fcpos[1]-120)/27)*3)
                allyears[currentyearpos].currentdaytracked=0
            elif 608<fcpos[0]<783 and 267<fcpos[1]<357:#change day
                clickedpos=[int(int((fcpos[0]-608)/25)%7),int(int((fcpos[1]-267)/15))]#on a 7x6 array
                #print clickedpos
                if clickedpos[1]==0:#first row clicked
                    if clickedpos[0]-allyears[currentyearpos].firstday[allyears[currentyearpos].currentmonthtracked]>=0:
                        allyears[currentyearpos].currentdaytracked=clickedpos[0]-allyears[currentyearpos].firstday[allyears[currentyearpos].currentmonthtracked]
                else:
                    newdaytrack=7-allyears[currentyearpos].firstday[allyears[currentyearpos].currentmonthtracked]+clickedpos[0]+(clickedpos[1]-1)*7
                    if newdaytrack<allyears[currentyearpos].monthlength[allyears[currentyearpos].currentmonthtracked]:
                        allyears[currentyearpos].currentdaytracked=newdaytrack
                #if 0<clickedpos+allyears[currentyearpos].firstday[allyears[currentyearpos].currentmonthtracked]<=allyears[currentyearpos].monthlength[allyears[currentyearpos].currentmonthtracked]:
            elif 95<fcpos[1]<116: #change year
                if 645<fcpos[0]<656 and currentyearpos:
                    currentyearpos-=1
                elif 715<fcpos[0]<726 and currentyearpos+1!=len(allyears):
                    currentyearpos+=1
