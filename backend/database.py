import mysql.connector


db = mysql.connector.connect(host="ec2-user@ip-172-31-17-246", user="ec2-user", passwd="", db="Music")
cursor = self.db.cursor()

add_log = ("INSERT INTO SpotifyArtist"
"(ArtistID, SongID, ArtistName, Genre)"
"VALUES (%s, %s, %s, %s)")

data = ("asdgasdg", "asdfkjfasd", "Filip", "Sad")

cursor.execute(add_log, data)
db.commit()
