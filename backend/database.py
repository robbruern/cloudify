import mysql.connector

def insert_recently_played(userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = self.db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID))

    isIn = False
    for (user) in cursor:
        isIn = True

    if(isIn):
        update_recent = ("UPDATE RecentlyPlayed "
        "SET SongID = %s, SongName = %s, Acousticness = %f, Danceability = %f, Energy = %f, Instrumentalness = %f, Liveness = %f, Speechiness = %f, Valence = %f, Tempo = %f, Genre = %s"
        "WHERE UserID = %s)")
        update_song_data = (songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre, userID)
        cursor.execute(update_recent, update_song_data)
    else:
        insert_recent = ("INSERT INTO RecentlyPlayed"
        "(UserID, SongID, SongName, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Speechiness, Valence, Tempo, Genre)"
        "VALUES (%s, %s, %s, %f, %f, %f, %f, %f, %f, %f, %f, %s)")
        insert_song_data = (userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre)
        cursor.execute(insert_recent, insert_song_data)

        insert_user = ("INSERT INTO RecentlyPlayed"
        "(UserID)"
        "VALUES (%s)")
        insert_user_data = (userID)
        cursor.execute(insert_user, insert_user_data)

    db.commit()
    cursor.close()
    db.close()
    return

def retrieve_recently_played(userID):
    pass

insert_recently_played("pog", "pog2", "pil", 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, "Country")
