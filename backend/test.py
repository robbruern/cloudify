import mysql.connector

print("got here")
db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
print("connected")
cursor = db.cursor()
print("help")
add_log = ("INSERT INTO SpotifyArtist"
"(ArtistID, SongID, ArtistName, Genre)"
"VALUES (%s, %s, %s, %s)")

data = ("asdgasdg", "asdfkjfasd", "Filip", "Sad")

cursor.execute(add_log, data)
db.commit()
exit()
