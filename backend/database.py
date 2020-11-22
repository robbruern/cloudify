import mysql.connector

def insert_recently_played(userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    if(isIn):
        update_recent = ("UPDATE RecentlyPlayed "
        "SET SongID = %s, SongName = %s, Acousticness = %s, Danceability = %s, Energy = %s, Instrumentalness = %s, Liveness = %s, Speechiness = %s, Valence = %s, Tempo = %s, Genre = %s"
        "WHERE UserID = %s")
        update_song_data = (songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre, userID)
        cursor.execute(update_recent, update_song_data)
    else:
        insert_recent = ("INSERT INTO RecentlyPlayed"
        "(UserID, SongID, SongName, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Speechiness, Valence, Tempo, Genre)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        insert_song_data = (userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre)
        cursor.execute(insert_recent, insert_song_data)

        insert_user = ("INSERT INTO ActiveUsers"
        "(UserID)"
        "VALUES (%s)")
        insert_user_data = (userID,)
        cursor.execute(insert_user, insert_user_data)

    db.commit()
    cursor.close()
    db.close()
    return

def retrieve_recently_played(userID):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    # User is not in Database
    if(isIn == False):
        return None

    query = ("SELECT * FROM RecentlyPlayed WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))
    
    ret = ()
    for tup in cursor:
        ret = tup

    db.commit()
    cursor.close()
    db.close()

    return ret

def delete_recently_played(userID):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    # User is not in Database
    if(isIn == False):
        return

    delete_recent = ("DELETE FROM RecentlyPlayed WHERE UserID LIKE %s")
    cursor.execute(delete_recent, (userID,))

    delete_user = ("DELETE FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(delete_user, (userID,))
    db.commit()
    cursor.close()
    db.close()
    return


def insert_song_table(cursor, insert_song_table):
    
    insert_song = ("INSERT IGNORE INTO SpotifySong"
        "(SongID, ArtistID, SongName, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Speechiness, Valence, Tempo)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.executemany(insert_song, insert_song_table)

def insert_artist_table(cursor, insert_artist_table):
    
    insert_artist = ("INSERT IGNORE INTO SpotifyArtist"
        "(ArtistID, ArtistName, Genre)"
        "VALUES (%s, %s, %s)")
    cursor.executemany(insert_artist, insert_artist_table)
    
    


# this method will also call insert_song_table so we can
# work with a collection of data later
def insert_user_favorite_songs(userID, userName, songInfoList):
    # list of (userID, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10])
    # (songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre)
    # should add ArtistID and ArtistsName 
    # later to s[11] and s[12] in songList

    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor(buffered = True)

    insert_user_song_data = []
    insert_song_data = []
    insert_artist_data = []
    for s in songInfoList:
        insert_user_song_data.append((userID, s[0]))
        insert_song_data.append((s[0], s[11], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9]))
        insert_artist_data.append((s[11], s[12], s[10]))

    insert_recent = ("INSERT IGNORE INTO UsersFavoriteSongs"
    "(UserID, SongID)"
    "VALUES (%s, %s)")
    cursor.executemany(insert_recent, insert_user_song_data)

    insert_song_table(cursor, insert_song_data)
    insert_artist_table(cursor, insert_artist_data)

    insert_user = ("INSERT IGNORE INTO ActiveUsers"
    "(UserID, Name)"
    "VALUES (%s, %s)")
    insert_user_data = (userID,userName)
    cursor.execute(insert_user, insert_user_data)

    db.commit()
    cursor.close()
    db.close()
    return

def delete_user(userID):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    # User is not in Database
    if(isIn == False):
        return

    delete_recent = ("DELETE FROM RecentlyPlayed WHERE UserID LIKE %s")
    cursor.execute(delete_recent, (userID,))

    delete_favorite = ("DELETE FROM UsersFavoriteSongs WHERE UserID LIKE %s")
    cursor.execute(delete_favorite, (userID,))

    delete_user = ("DELETE FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(delete_user, (userID,))
    db.commit()
    cursor.close()
    db.close()
    return

# will return a list of song IDs
# takes ID of friend and number of songs for playlist
# if there aren't enough songs, will return max
# but it shoudlnt be an issue once we have enough data
def build_friends_recommended_playlist(friendID, numSongs):
    db = mysql.connector.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT AVG(Acousticness), AVG(Danceability), AVG(Energy), AVG(Instrumentalness),"
    "AVG(Liveness), AVG(Speechiness), AVG(Valence), AVG(Tempo)" 
    "FROM UsersFavoriteSongs NATURAL JOIN SpotifySong"
    "WHERE UserID LIKE %s")
    cursor.execute(query, (friendID,))

    isIn = False
    for item in cursor:
        isIn = True
        print(item)
    return 

data = []
data.append(("1234", "sad", 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,"sad again", "23232", "Lil Beep"))
data.append(("4321", "happy", 0.1,0.9,0.3,0.7,0.5,0.6,0.4,0.8,"not sad", "23232", "Biggy Wiggy"))
insert_user_favorite_songs("test", "helperino", data)
build_friends_recommended_playlist("test", 1)
#delete_user("test")

    

