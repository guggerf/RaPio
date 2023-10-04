#####################################################
####Diplomarbeit fuer TEKO als Elektrotechniker HF###
#####By guggerf      ################################
#####################################################
# V1.0
#Alle Funktionen implementiert
#Debugging braucht noch mehr Zeit!

#Benoetigte Module importieren
import pygame
from pygame.locals import *
import time, datetime, subprocess, os, glob, math

#Klasse fuer Buttons definieren
class Button(object):
    #Konstruktor
	def __init__(self, x, y, visible, imageFile, callback):
		self.x = x
		self.y = y
		self.visible = visible
		self.callback = callback
		self.imageObject = pygame.image.load(imageFile)
	#Den Button auf dem Screen anzeigen
	def draw(self, screen):
		if self.visible:
			screen.blit(self.imageObject, (self.x, self.y))
	#Zone definieren wo der Button gedrueckt werden kann
	def clicked(self, clickPos):
		return self.visible and self.x <= clickPos[0] <= self.x + buttonSize and self.y <= clickPos[1] <= self.y + buttonSize
	#Aktion ausfuehren wenn Button gedrueckt wird
	def onClick(self):
		print "onClick of button " + str(self.callback) #debugging
		
		#wenn Button nicht sichtbar ist, keine Aktion ausfuehren
		if not self.visible:
			return		
		#Option dass eintwerder ein String oder eine Funktion angewendet werden kann		
		if type(self.callback) is str:
			subprocess.call(self.callback, shell=True) #z.b. fuer MPC zu steuern
		else:
			self.callback()
#Funktion fuer die Erkennung einer Beruehrung am Screen
def on_click():
	clickPos = pygame.mouse.get_pos()
	print "screen touched at " + str(clickPos[0]) + "x" + str(clickPos[1]) #debugging
	
	#Clicked Flag in Buttons auf Home-Screen setzten
	for homeButton in homeButtons:
		if homeButton.clicked(clickPos):
			homeButton.onClick()			
	#Clicked Flag in Buttons auf Alarm-Screen setzten
	for alarmButton in alarmButtons:
		if alarmButton.clicked(clickPos):
			alarmButton.onClick()
        #Clicked Flag in Buttons auf sleep-Screen setzten
	for sleepButton in sleepButtons:
		if sleepButton.clicked(clickPos):
			sleepButton.onClick()	
#Wecker oder Sleep einschalten
def alarmOn():
        #Um mit Gobalen Variablen in verschiedenen Funktionen zu arbeiten
        #muessen diese in der jeweiligen Funktion eingelesen werden
        global statusAlarm, statusSleep, statusScreen, alarmTime_h, alarmTime_min, sleepTime_h, sleepTime_min
        global timeNowSec, timeStampSleep, sleepInSec, alarmDays
        #Aktion von Wecker
        for i in alarmDays:
                if i == True and statusScreen == 1: 
                        statusAlarm = True
        #Aktion von Sleep
        if statusScreen == 2:
                statusSleep = True
                #Timestamp in sekunden von jetzt
                timeStampSleep = timeNowSec
                print "Aktueller TimeStamp: ", timeStampSleep
                #Zeiten umrechnen in sekunden
                sleepInSec = ((sleepTime_h * 3600)+(sleepTime_min * 60)+timeStampSleep)
                print "Sleep am: ", sleepInSec                
	refresh_home_screen()	
	return timeStampSleep, sleepInSec

#Wecker oder Sleep ausschalten	
def alarmOff():
	global statusAlarm, statusSleep, statusScreen, alarmTime_h, alarmTime_min, sleepTime_h, sleepTime_min
	if statusScreen == 1: 
                statusAlarm = False
                alarmTime_h = 0
                alarmTime_min = 0
        if statusScreen == 2:
                statusSleep = False
                sleepTime_h = 0
                sleepTime_min = 0                
	refresh_home_screen()
        return alarmTime_h, alarmTime_min, sleepTime_h, sleepTime_min

#Stunden auswaehlen um zu veraendern
def setHour():
    global statusAlarmSetHour
    statusAlarmSetHour = True
        
#Minuten auswaehlen um zu veraendern
def setMin():
    global statusAlarmSetHour
    statusAlarmSetHour = False

#Mit Button Up Min oder Stunden verstellen
def buttonUp():
        global alarmTime_h, alarmTime_min, statusAlarmSetHour, sleepTime_h, sleepTime_min

        if statusScreen == 1:
                if statusAlarmSetHour == True:
                        alarmTime_h = alarmTime_h + 1
                        if alarmTime_h > 23:
                                alarmTime_h = 0
                else:
                        alarmTime_min = alarmTime_min + 5
                        if alarmTime_min > 55:
                                alarmTime_min = 0
        if statusScreen == 2:
                if statusAlarmSetHour == True:
                        sleepTime_h = sleepTime_h + 1
                        if sleepTime_h > 23:
                                sleepTime_h = 0
                else:
                        sleepTime_min = sleepTime_min + 1
                        if sleepTime_min > 59:
                                sleepTime_min = 0

        return alarmTime_h, alarmTime_min, sleepTime_h, sleepTime_min

#Mit Button Down Min oder Stunden verstellen
def buttonDown():
        global alarmTime_h, alarmTime_min, statusAlarmSetHour, sleepTime_h, sleepTime_min
        
        if statusScreen == 1:#wenn in Alarm-Screen
                if statusAlarmSetHour == True:
                        alarmTime_h = alarmTime_h - 1
                        if alarmTime_h < 0:
                                alarmTime_h = 23
                else:
                        alarmTime_min = alarmTime_min - 5
                        if alarmTime_min < 0:
                                alarmTime_min = 55
        if statusScreen == 2:#wenn in Sleep-Screen
                if statusAlarmSetHour == True:
                        sleepTime_h = sleepTime_h - 1
                        if sleepTime_h < 0:
                                sleepTime_h = 23
                else:
                        sleepTime_min = sleepTime_min - 1
                        if sleepTime_min < 0:
                                sleepTime_min = 59

        return alarmTime_h, alarmTime_min, sleepTime_h, sleepTime_min
                        
#Funktionen um Tag ein- oder ausschalten fuer Wecker
def buttonAlarmDayMo():
        global alarmDays, statusAlarmDayMo
        statusAlarmDayMo =not statusAlarmDayMo #toogle Status
        
        if statusAlarmDayMo == True:
                alarmDays[1] = True
        else:
                alarmDays[1] = False
        print alarmDays#debugging
        
def buttonAlarmDayDi():
        global alarmDays, statusAlarmDayDi
        statusAlarmDayDi =not statusAlarmDayDi
        if statusAlarmDayDi == True:
                alarmDays[2] = True
        else:
                alarmDays[2] = False
        
def buttonAlarmDayMi():
        global alarmDays, statusAlarmDayMi
        statusAlarmDayMi =not statusAlarmDayMi
        if statusAlarmDayMi == True:
                alarmDays[3] = True
        else:
                alarmDays[3] = False
        
def buttonAlarmDayDo():
        global alarmDays, statusAlarmDayDo
        statusAlarmDayDo =not statusAlarmDayDo
        if statusAlarmDayDo == True:
                alarmDays[4] = True
        else:
                alarmDays[4] = False
        
def buttonAlarmDayFr():
        global alarmDays, statusAlarmDayFr
        statusAlarmDayFr =not statusAlarmDayFr
        if statusAlarmDayFr == True:
                alarmDays[5] = True
        else:
                alarmDays[5] = False
                
def buttonAlarmDaySa():
        global alarmDays, statusAlarmDaySa
        statusAlarmDaySa =not statusAlarmDaySa
        if statusAlarmDaySa == True:
                alarmDays[6] = True
        else:
                alarmDays[6] = False
                                
def buttonAlarmDaySo():
        global alarmDays, statusAlarmDaySo
        statusAlarmDaySo =not statusAlarmDaySo
        if statusAlarmDaySo == True:
                alarmDays[0] = True
        else:
                alarmDays[0] = False
                
#Funktion um Tages-Button im Alarm-Screen zu tauschen wenn angewaehlt oder nicht
def toogleDayButtons(status, btn1, btn2):
        if status == True:
                btn1.visible = False
                btn2.visible = True
        else:
                btn1.visible = True
                btn2.visible = False
                
#Funktion welche ueberprueft ob Sleep aktive ist und diesen ausfuehren
def sleep():
        global timeNow, timeNowSec, sleepTime_h, sleepTime_min, statusSleep, timeSleepDifference, sleepInSec
        global timeStampSleep, statusBacklight
        
        if statusSleep == True and timeStampSleep > 0:
                if statusBacklight == 2:
                        backlightDim(0)#Backlight ganz aus
                timeSleepDifference = abs (sleepInSec - timeNowSec)#Differenz berechnen
                print "Sleep in: %s Sekunden" %(timeSleepDifference)#debugging
                
                if timeNowSec == sleepInSec:#wenn Zeit erreicht wurde
                        statusSleep = False
                        count = 90
                        while count > 0:#Volumen von 90 auf 0 in 1er Schritten
                                subprocess.call("mpc volume -1 ", shell=True)
                                count = count - 1
                        subprocess.call("mpc stop", shell=True)
                        subprocess.call("mpc volume 90 ", shell=True)
                        sleepInSec = 0
                        timeStampSleep = 0
                        backlightDim(0)#Backlight ganz aus
                return timeSleepDifference
        
#Funktion welche ueberprueft ob Wecker aktiv und diesen ausloest        
def alarm():
        global timeNow, dayNow, alarmTime_h, alarmTime_min, statusAlarm, satusAlarmDay, alarmDays
        if statusAlarm == True and alarmDays[dayNow] == True:                
                if timeNow.hour == alarmTime_h and timeNow.minute == alarmTime_min:
                        subprocess.call("mpc volume 0 ", shell=True)
                        subprocess.call("mpc play 3", shell=True)
                        refresh_home_screen()
                        count = 90
                        while count > 0:
                                subprocess.call("mpc volume +1 ", shell=True)
                                count = count - 1
                        statusAlarm = False #nicht gewuenscht da der wecker noch weiter aktiv sein soll
#Zeit aktualisieren
def getTime():
        global timeNow, timeNowSec, dayNow
        timeNow = datetime.datetime.now()#genaue Zeit
        dayNow = int(time.strftime("%w"))#Zahl des Wochentages als int
        timeNowSec = math.floor(time.time()) #gerundet auf ganze sekunden
        return timeNow, timeNowSec, dayNow

#Funktion fuer Grundbild von Wecker und Sleep Screen
def loadHead(headText):
        #Texts and Labels
	font80=pygame.font.Font(None,80)#Schriftgroesse 80 initialisieren
	font34=pygame.font.Font(None,34)#Schriftgroesse 34 initialisieren
	font24=pygame.font.Font(None,24)#Schriftgroesse 24 initialisieren
	lb_titel=font34.render(headText, 1, (green))
	screen.blit(lb_titel,(5, 5)) #headText darstellen

	#Zeit und Datum anzeigen
	lb_date=font24.render(time.strftime("%d.%b.%Y"), 1, (white))
	lb_time=font24.render(time.strftime("%H:%M"), 1, (white))
	screen.blit(lb_date, (5, 30))
	screen.blit(lb_time, (110, 30))

	#Rahmen und Linien zeichnen
	pygame.draw.rect(screen, green, (0,0,320,240),3) #Rahmen aussen
	pygame.draw.line(screen, green, (0,55),(320,55),3) #Obere Linie

	#entscheiden wo ob Minuten oder Stunden veraendert werden
	if statusAlarmSetHour == True:
                pygame.draw.rect(screen, green, (80,82,70,65),1) #Rahmen Stunden
        else:
                pygame.draw.rect(screen, green, (175,82,70,65),1) #Rahmen Minuten
                
#Funktion um die Hintergrundbeleuchtung zu steuern
def backlightDim(value):
        #Value 0 = Backlight aus
        #Value 1-255 = Helligkeit fuer Backlight
        global statusBacklight
        
        if value >= 255:
                value = 255#um eine groessere Zahl zu vermeiden, da sonst Probleme mit PWM auftreten koennen
                statusBacklight = 1
        elif value == 0:
                statusBacklight = 0
        else:
                statusBacklight = 2
        #Konsolenbefehl mit subprocess.call ausfuehren        
        subprocess.call("sudo echo %s > /sys/class/backlight/4dpi/brightness" %(value), shell=True)
        
        return statusBacklight

#Funktion um zu schauen ob eine Wiedergabe laeuft
def playing():
	station = subprocess.check_output("mpc current", shell=True )
	lines=station.split(":")
	return lines[0] != "";

############################################################
#Funktion um Home-Screen zu zeichnen
def refresh_home_screen():
	global statusAlarm, statusSleep, statusScreen, timeSleepDifference
	
	statusScreen = 0 #Statuswert fuer Home-Screen
	screen.fill(black) #Hintergrundfarbe
	
	#Texts and Labels
	font40=pygame.font.Font(None,40)
	font34=pygame.font.Font(None,34)
	font24=pygame.font.Font(None,24)
	font20=pygame.font.Font(None,20)
	lb_titel=font34.render("RaPio", 1, (green))
	lb_autor=font24.render("by F.Gugger", 1, (green))
	screen.blit(lb_titel,(5, 5))
	screen.blit(lb_autor,(5, 30))
	
	#Rahmen und Linien zeichnen
	pygame.draw.rect(screen, green, (0,0,320,240),3) #Rahmen aussen
	pygame.draw.line(screen, green, (0,55),(320,55),3) #Obere Linie
	pygame.draw.line(screen, green, (0,125),(320,125),3) #mittlere Linie
	pygame.draw.line(screen, green, (0,170),(320,170),3) #untere Linie

	#Zeit und Datum anzeigen
	lb_date=font24.render(time.strftime("%d.%b.%Y"), 1, (white))
	lb_time=font24.render(time.strftime("%H:%M"), 1, (white))
	screen.blit(lb_date, (120, 30))
	screen.blit(lb_time, (225, 30))
	
	#Die Buttons auf dem Home-Screen laden
	for homeButton in homeButtons:
		homeButton.draw(screen)
		homeButton.visible = True
	#Die Alarm Buttons auf dem Home-Screen verbergen
	for alarmButton in alarmButtons:
		alarmButton.visible = False
	#Die sleep Buttons auf dem Home-Screen verbergen
	for sleepButton in sleepButtons:
		sleepButton.visible = False
	
	#Play und Stop Button anzeigen oder nicht
	if not playing():
		btnPlay.visible = True
		btnStop.visible = False
		title = "druecke PLAY"
	else:
		btnPlay.visible = False
		btnStop.visible = True
	
	#Status Alarm und Sleep anzeigen
	if statusAlarm == True:
                lb_alarmOn = font24.render("Wecker", 1, green)
                screen.blit(lb_alarmOn, (110, 63))
		
	if statusSleep == True:
                text_min = int(timeSleepDifference / 60)
                if timeSleepDifference < 60:#wenn unter 1 min, verbleibende Sekunden anzeigen
                        textSleep = "Sleep in: %s sek" %(int(timeSleepDifference))
                else:
                        textSleep = "Sleep in: %s Min" %(text_min)#Verbleibende Minuten anzeigen
                        
                lb_sleepOn = font24.render(textSleep, 1, green)
                screen.blit(lb_sleepOn, (180, 63))
                
	#Den Stations- und Titelname auslesen und trennen: 
	station = subprocess.check_output("mpc current", shell=True )
	lines=station.split(":")#Text bei einem : in zwei Zeilen teilen
	length = len(lines) 
	if length == 1:#Wenn nur eine Zeile vorhanden wird vom Stream keine Infos gesendet
		line1 = lines[0]
		line1 = line1[:-1] #Letztes Zeichen loeschen, ist immer ein ?
		line2 = "keine Infos"
	else:
		line1 = lines[0]
		line2 = lines[1]
		line2 = line2[1:]
		line2 = line2[:-1] #Letztes Zeichen loeschen, ist immer ein ?
	
	if line1.find(" -") >= 0: #Alles hinter - ausschneiden
		station = line1[:line1.find(" -")]#um Senderdetail nicht anzuzeigen
	else:
		station = line1
	#Die Laenge vom Titel kuerzen wegen Screen Breite
	title = line2[:35]#Je nach Buchstaben/Zeichen reicht dies noch nicht
	
	#Sendername anzeigen
	lb_station = font24.render("Sender:", 1, (white))
	screen.blit(lb_station, (10, 63))
	station_name=font40.render(station, 1, (white))
	screen.blit(station_name,(10,85))
	#Zusatzinfos anzeigen
	lb_additionalData = font20.render("Interpret - Titel:", 1, (white))
        screen.blit(lb_additionalData, (10, 130))
	additional_data=font24.render(title, 1, (white))
	screen.blit(additional_data,(10, 145))
	
	#Die Netzwerk ID auslesen und anzeigen in welchem Netz sich der Rapio befindet
	network_id = subprocess.check_output("wpa_cli status | grep id_str | cut '-d=' -f 2 | tr -d '\n'", shell=True )
	
	#Netzwerkverbindung ueberpruefen (es wird nur auf die IP geachtet)
	IP = subprocess.check_output("hostname -I", shell=True )
	IP=IP[:3]
	if IP == "192" and network_id != "":
		status_color = green
	else:
		if network_id == "":
			network_id = "offline"		
                status_color = red

	network_name_label = font24.render("Netzwerk:", 1, (white))
	network_status_label = font24.render(network_id, 1, (status_color))
	screen.blit(network_name_label, (120, 10))
	screen.blit(network_status_label, (205,10))
	
	pygame.display.flip()

############################################################
#Funktion um Alarm-Screen zu zeichnen
def refresh_alarm_screen():
        global timeNow, alarmTime_h, alarmTime_min, statusScreen
        
	statusScreen = 1 #Status auf alarm setzten
	
	screen.fill(black) #Hintergrundfarbe
	
	#Die Buttons vom Home-Screen verbergen
	for homeButton in homeButtons:
		homeButton.visible = False

	#Die Buttons auf dem Alarm-Screen laden
	for alarmButton in alarmButtons:
		alarmButton.draw(screen)
		alarmButton.visible = True
		
        #Check ob Tag grau oder rot angezeigt werden soll
	toogleDayButtons(statusAlarmDayMo, btnMo, btnMoRed)
	toogleDayButtons(statusAlarmDayDi, btnDi, btnDiRed)
	toogleDayButtons(statusAlarmDayMi, btnMi, btnMiRed)
	toogleDayButtons(statusAlarmDayDo, btnDo, btnDoRed)
        toogleDayButtons(statusAlarmDayFr, btnFr, btnFrRed)
        toogleDayButtons(statusAlarmDaySa, btnSa, btnSaRed)
        toogleDayButtons(statusAlarmDaySo, btnSo, btnSoRed)
	
	loadHead(headAlarm)
	
	#Zeitauswahl zeichnen und in String umwandeln
	alarmStrTime_h = str(alarmTime_h)
        if len(alarmStrTime_h) < 2: #wenn Stunden nur einstellig wird eine 0 vordran gehaengt
                alarmStrTime_h = "0" + alarmStrTime_h
			
	alarmStrTime_min = str(alarmTime_min)
        if len(alarmStrTime_min) < 2: #wenn Minuten nur einstellig wird eine 0 vordran gehaengt
		alarmStrTime_min = "0" + alarmStrTime_min

        font80=pygame.font.Font(None,80)        
	lb_alarmTime_h=font80.render(alarmStrTime_h , 1, (white))
	screen.blit(lb_alarmTime_h, (85, 82))
	lb_alarmTimeSpace=font80.render(":", 1, (white))
	screen.blit(lb_alarmTimeSpace, (157, 82))
	lb_alarmTime_min=font80.render(alarmStrTime_min, 1, (white))
	screen.blit(lb_alarmTime_min, (180, 82))

	pygame.display.flip()

############################################################
#Funktion um Sleep-Screen zu zeichnen
def refresh_sleep_screen():
        global timeNow, sleepTime_h, sleepTime_min, statusScreen
        
	statusScreen = 2 #Status auf sleep setzten
	
	screen.fill(black) #Hintergrundfarbe
	
	#Die Buttons vom Home-Screen verbergen
	for homeButton in homeButtons:
		homeButton.visible = False

	#Die Buttons auf dem Sleep-Screen laden
	for sleepButton in sleepButtons:
		sleepButton.draw(screen)
		sleepButton.visible = True

	loadHead(headSleep)
	
	#Zeitauswahl zeichnen und in String umwandeln
	sleepStrTime_h = str(sleepTime_h)
        if len(sleepStrTime_h) < 2: #wenn Stunden nur einstellig wird eine 0 vordran gehaengt
                sleepStrTime_h = "0" + sleepStrTime_h
			
	sleepStrTime_min = str(sleepTime_min)
        if len(sleepStrTime_min) < 2: #wenn Minuten nur einstellig wird eine 0 vordran gehaengt
		sleepStrTime_min = "0" + sleepStrTime_min

        font80=pygame.font.Font(None,80)        
	lb_sleepTime_h=font80.render(sleepStrTime_h , 1, (white))
	screen.blit(lb_sleepTime_h, (85, 82))
	lb_sleepTimeSpace=font80.render(":", 1, (white))
	screen.blit(lb_sleepTimeSpace, (157, 82))
	lb_sleepTime_min=font80.render(sleepStrTime_min, 1, (white))
	screen.blit(lb_sleepTime_min, (180, 82))

	pygame.display.flip()
#Hauptfunktion mit Loop-Schleife 	 
def main():
        global timeNow, timeNowSec, timeStampLastTouch, statusBacklight
	while 1:#Loop-Schleife
		for event in pygame.event.get():
			#Druck auf Touchscreen registrieren
			if event.type == pygame.MOUSEBUTTONDOWN:
                                if statusBacklight == 0: #wenn BL aus, soll noch kein Button gedrueckt werden koennen
                                        timeStampLastTouch = timeNowSec
                                        backlightDim(255)
                                else:
                                        timeStampLastTouch = timeNowSec
                                        backlightDim(255) #Backlight auf 255 setzten, einschalten
                                        on_click()

		#Backlight ausschalten wenn keine Beruehrung innerhalb 1 min
		if statusBacklight == 1:
                        if timeStampLastTouch == 0: #Ganz am Anfang vom Programm-Ablauf
                                timeStampLastTouch = timeNowSec
                        timeBLDim = timeStampLastTouch + 10
                        timeDifference = abs (timeBLDim - timeNowSec)
                        print "Backlight aus in: %s Sekunden" %(timeDifference)#debugging
                        if timeNowSec == timeBLDim:
                                backlightDim(10) #Backlight auf 10 zurueck dimmen
                if statusBacklight == 2:#wenn Backlight gedimmt, nach 5 Min ganz ausschalten
                        timeBLOFF = timeStampLastTouch + 300
                        if timeNowSec == timeBLOFF:
                                backlightDim(0) #Backlight ausschalten
		if statusScreen == 0:
			refresh_home_screen()
		elif statusScreen == 1:
			refresh_alarm_screen()
		elif statusScreen == 2:
                        refresh_sleep_screen()			
		
		getTime()#Zeit aktualisieren
		sleep()#Schauen ob Sleep-Timer on
		alarm()	#Schauen ob alarm on
		time.sleep(0.05)#warten fuer 0.5 Sekunden
		pygame.display.update()

#Alles wurde nun Initialisiert und die Aufrufe koennen beginnen
os.environ["SDL_FBDEV"] = "/dev/fb1" #Displayausgang waehlen fb1= SPI
os.environ["SDL_MOUSEDEV"] = "/dev/input/event0" #Treiber fuer Touchscreen
os.environ["SDL_MOUSEDRV"] = "TSLIB"

size = width, height = 320, 240 #Groesse des Displays
pygame.init()
pygame.mouse.set_visible(False) #Mauszeiger verbergen
screen = pygame.display.set_mode(size)

#Farben defineieren
blue = 26, 0, 255
black = 0, 0, 0
white = 255, 255, 255
green = 0, 255, 0

#Status in welchem Screen sich das Program befindet
statusScreen = 0 #0=home / 1= alarm / 2=sleep
#Status Alarm
statusAlarm = False #False = off / True = on
#Status Sleep
statusSleep = False #False = off / True = on
#Status fuer Zeiteinstellung Wecker
statusAlarmSetHour = True #True = Stunden verstellen / False = Minuten verstellen
#Status ob Backlight an oder aus
statusBacklight = 1 #1 = ein / 2 = gedimmt / 0 = aus

#Zeitstempel fuer Erkennung wann der Bildschirm zulezt beruert wurde
timeStampLastTouch = 0

#Variablen fuer Alarm
timeNow = 0
dayNow = 0
alarmTime_h = 0
alarmTime_min = 0
headAlarm = "Wecker stellen"
#Position 0 = So / Position 6 = Sa 
alarmDays = [False, False, False, False, False, False, False, ]
#Status Wecker jeweiligen Tag ein
statusAlarmDayMo = False #True = Wecker Mo ein / False = wecker aus
statusAlarmDayDi = False
statusAlarmDayMi = False
statusAlarmDayDo = False
statusAlarmDayFr = False
statusAlarmDaySa = False
statusAlarmDaySo = False

#Variablen fuer Sleep
timeNowSec = 0
sleepTime_h = 0
sleepTime_min = 0
headSleep = "Sleep-Timer stellen"
timeSleepDifference = 0
sleepInSec = 0
timeStampSleep = 0

buttonSize = 40
#Liste mit Buttons fuer Home-Screen erstellen
homeButtons = []
btnPlay = Button(74, 180, False, "img/home/play.png", "mpc play")
btnStop = Button(74, 180, False, "img/home/stop.png", "mpc stop")
homeButtons.append(btnPlay)
homeButtons.append(btnStop)
homeButtons.append(Button(12, 180, True, "img/home/previous.png", "mpc prev"))
homeButtons.append(Button(136, 180, True, "img/home/next.png", "mpc next"))
homeButtons.append(Button(198, 180, True, "img/home/alarm.png", refresh_alarm_screen))
homeButtons.append(Button(260, 180, True, "img/home/sleep.png", refresh_sleep_screen))

#Liste mit Buttons fuer Alarm-Screen erstellen
alarmButtons = []
alarmButtons.append(Button(15, 65, True, "img/alarm/up.png", buttonUp))
alarmButtons.append(Button(15,120, True, "img/alarm/down.png", buttonDown))
alarmButtons.append(Button(255, 65 , True, "img/alarm/on.png", alarmOn))
alarmButtons.append(Button(255, 120 , True, "img/alarm/off.png", alarmOff))
alarmButtons.append(Button(100, 85, True, "img/alarm/blank.png", setHour))#fuer Stunden waehlen
alarmButtons.append(Button(190, 90, True, "img/alarm/blank.png", setMin))#fuer Minuten waehlen
#Tages buttons zu Liste hinzufuegen
btnMo = Button(5, 185, True, "img/alarm/mo_gray.png", buttonAlarmDayMo)
btnMoRed = Button(5, 185, True, "img/alarm/mo_red.png", buttonAlarmDayMo)
btnDi = Button(50, 185, True, "img/alarm/di_gray.png", buttonAlarmDayDi)
btnDiRed = Button(50, 185, True, "img/alarm/di_red.png", buttonAlarmDayDi)
btnMi = Button(95, 185, True, "img/alarm/mi_gray.png", buttonAlarmDayMi)
btnMiRed = Button(95, 185, True, "img/alarm/mi_red.png", buttonAlarmDayMi)
btnDo = Button(140, 185, True, "img/alarm/do_gray.png", buttonAlarmDayDo)
btnDoRed = Button(140, 185, True, "img/alarm/do_red.png", buttonAlarmDayDo)
btnFr = Button(185, 185, True, "img/alarm/fr_gray.png", buttonAlarmDayFr)
btnFrRed = Button(185, 185, True, "img/alarm/fr_red.png", buttonAlarmDayFr)
btnSa = Button(230, 185, True, "img/alarm/sa_gray.png", buttonAlarmDaySa)
btnSaRed = Button(230, 185, True, "img/alarm/sa_red.png", buttonAlarmDaySa)
btnSo = Button(275, 185, True, "img/alarm/so_gray.png", buttonAlarmDaySo)
btnSoRed = Button(275, 185, True, "img/alarm/so_red.png", buttonAlarmDaySo)
alarmButtons.append(btnMo)
alarmButtons.append(btnMoRed)
alarmButtons.append(btnDi)
alarmButtons.append(btnDiRed)
alarmButtons.append(btnMi)
alarmButtons.append(btnMiRed)
alarmButtons.append(btnDo)
alarmButtons.append(btnDoRed)
alarmButtons.append(btnFr)
alarmButtons.append(btnFrRed)
alarmButtons.append(btnSa)
alarmButtons.append(btnSaRed)
alarmButtons.append(btnSo)
alarmButtons.append(btnSoRed)

#Liste mit buttons fuer Sleep-Screen erstellen
sleepButtons = []
sleepButtons.append(Button(15, 65, True, "img/alarm/up.png", buttonUp))
sleepButtons.append(Button(15,120, True, "img/alarm/down.png", buttonDown))
sleepButtons.append(Button(255, 65 , True, "img/alarm/on.png", alarmOn))
sleepButtons.append(Button(255, 120 , True, "img/alarm/off.png", alarmOff))
sleepButtons.append(Button(100, 85, True, "img/alarm/blank.png", setHour))#fuer Stunden waehlen
sleepButtons.append(Button(190, 90, True, "img/alarm/blank.png", setMin))#fuer Minuten waehlen
	
#Beginnen
backlightDim(255) #Damit Backlight an ist
main() #Hauptschleife beginnen


