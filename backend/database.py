import mysql.connector

print("got here")
db = mysql.connector.connect(host="172.31.17.246",user="root",passwd="",db="Music",port="3306")
print("connected")
cursor = self.db.cursor()
print("help")
add_log = ("INSERT INTO SpotifyArtist"
"(ArtistID, SongID, ArtistName, Genre)"
"VALUES (%s, %s, %s, %s)")

data = ("asdgasdg", "asdfkjfasd", "Filip", "Sad")

cursor.execute(add_log, data)
db.commit()
exit()
