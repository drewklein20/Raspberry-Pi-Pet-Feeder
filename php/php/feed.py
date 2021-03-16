#!/usr/bin/env python2.7

import pigpio
import time
import mysql.connector
pi = pigpio.pi() # Connect to local Pi.

mydb = mysql.connector.connect(
  host="localhost",
  user="remote",
  password="PetFeeder2021!",
  database="Feeder"
)

dbcursor = mydb.cursor()
dbcursor.execute("SELECT * FROM Feeder.Weights order by id desc limit 1;")
dbresult = dbcursor.fetchone()
currentWeight = dbresult[1]

dbcursor = mydb.cursor()
dbcursor.execute("SELECT * FROM Logs ORDER BY id desc LIMIT 1")
dbresult = dbcursor.fetchone()
feedCups = dbresult[2]

dbcursor = mydb.cursor()
dbcursor.execute("SELECT JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.cupDuration')) as cupDuration, JSON_UNQUOTE(JSON_EXTRACT(preferences, '$.bowlWeight')) as cupDuration FROM Feeder.Settings;")
dbresult = dbcursor.fetchone()
cupDuration = dbresult[0]
fullBowlWeight = dbresult[1]

sleepAmount = float(cupDuration) * float(feedCups)

print(currentWeight)
print(fullBowlWeight)
if currentWeight < fullBowlWeight:
	try:
		pi.set_servo_pulsewidth(17, 2000)
		time.sleep(sleepAmount)
		# switch servo off
		pi.set_servo_pulsewidth(17, 0);
		pi.stop()

	except KeyboardInterrupt:
        	GPIO.cleanup()
