import pymysql
#import mysql.connector
import heapq


def insert_recently_played(userID, songID, songName, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers NATURAL JOIN RecentlyPlayed WHERE UserID LIKE %s")
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

    db.commit()
    cursor.close()
    db.close()
    return

def retrieve_active_users():
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID, Name FROM ActiveUsers")
    cursor.execute(query)

    ret = []
    for tup in cursor:
        ret.append(tup)

    db.commit()
    cursor.close()
    db.close()

    return ret

def retrieve_active_userIDs():
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers")
    cursor.execute(query)

    ret = []
    for tup in cursor:
        ret.append(tup[0])

    db.commit()
    cursor.close()
    db.close()

    return ret

def retrieve_shows():
    db = pymysql.connect(host='127.0.0.1', database='Music', user='root', password='eiHY?srFG70V')
    cursor = db.cursor()
    query = ('SELECT ShowID, ShowName FROM SpotifyShow')
    cursor.execute(query)


    ret = {}
    for tup in cursor:
        ret[tup[0]] = tup[1]

    db.commit()
    cursor.close()
    db.close()

    return ret

def retrieve_show_ids():
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT ShowID FROM SpotifyShow")
    cursor.execute(query)

    shows = []
    for show in cursor:
        shows.append(show[0])
    db.commit()
    cursor.close()
    db.close()
    return shows

def retrieve_active_userNameID():
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID, Name FROM ActiveUsers")
    cursor.execute(query)

    ret = {}
    for tup in cursor:
        ret[tup[0]] = tup[1]

    db.commit()
    cursor.close()
    db.close()

    return ret

def retrieve_artistIDs():
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT ArtistID FROM SpotifyArtist")
    cursor.execute(query)

    ret = []
    for tup in cursor:
        ret.append(tup[0])

    db.commit()
    cursor.close()
    db.close()

    return ret

def retrieve_recently_played(userID):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    # User is not in Database
    if(isIn == False):
        return None

    query = ("SELECT SongName FROM RecentlyPlayed WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))
    
    ret = []
    for tup in cursor:
        ret.append(tup)

    db.commit()
    cursor.close()
    db.close()

    return ret

def delete_recently_played(userID):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    query = ("SELECT UserID FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(query, (userID,))

    isIn = False
    for (user) in cursor:
        isIn = True

    # User is not in Database
    if(isIn == False):
        return

    delete_recent = ("DELETE FROM UsersFavoriteSongs WHERE UserID LIKE %s")
    cursor.execute(delete_recent, (userID,))

    delete_user = ("DELETE FROM ActiveUsers WHERE UserID LIKE %s")
    cursor.execute(delete_user, (userID,))
    db.commit()
    cursor.close()
    db.close()
    return


def insert_song_table(cursor, insert_song_table):
    
    insert_song = ("INSERT IGNORE INTO SpotifySong"
        "(SongID, ArtistID, SongName, Acousticness, Danceability, Energy, Instrumentalness, Liveness, Speechiness, Valence, Tempo, uri)"
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor.executemany(insert_song, insert_song_table)

def insert_artist_table(cursor, insert_artist_table):
    
    insert_artist = ("INSERT IGNORE INTO SpotifyArtist"
        "(ArtistID, ArtistName, Genre)"
        "VALUES (%s, %s, %s)")
    cursor.executemany(insert_artist, insert_artist_table)

def insert_show(showList):
    print("inserting show")
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()
    insert_show = ("INSERT IGNORE INTO SpotifyShow"
            "(ShowID, ShowName)"
            "VALUES (%s, %s)")
    cursor.executemany(insert_show, showList)
    db.commit()
    cursor.close()
    db.close()
    print("show inserted")
    return

def insert_user(userID, userName):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()
    insert_user = ("INSERT IGNORE INTO ActiveUsers"
    "(UserID, Name)"
    "VALUES (%s, %s)")
    insert_user_data = (userID,userName)
    cursor.execute(insert_user, insert_user_data)

    db.commit()
    cursor.close()
    db.close()
    return


# this method will also call insert_song_table so we can
# work with a collection of data later
def insert_user_favorite_songs(userID, userName, songInfoList):
    # list of (userID, s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[11])
    # (songID, songName, uri, acousticness, danceability, energy, instrumentalness, liveness, speechiness, valence, tempo, genre)
    # should add ArtistID and ArtistsName 
    # later to s[12] and s[13] in songList

    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    print(userID)
    print(userName)
    # for s in songInfoList:
    #     print(s)

    insert_user_song_data = []
    insert_song_data = []
    insert_artist_data = []
    for s in songInfoList:
        insert_user_song_data.append((userID, s[0]))
        insert_song_data.append((s[0], s[12], s[1], s[3], s[4], s[5], s[6], s[7], s[8], s[9], s[10], s[2]))
        insert_artist_data.append((s[12], s[13], s[11]))

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
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
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
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    # retrive avg values for every song's float parameters
    agg_query = ("SELECT AVG(Acousticness), AVG(Danceability), AVG(Energy), AVG(Instrumentalness),"
    " AVG(Liveness), AVG(Speechiness), AVG(Valence), AVG(Tempo)" 
    " FROM UsersFavoriteSongs NATURAL JOIN SpotifySong"
    " WHERE UserID LIKE %s")
    cursor.execute(agg_query, (friendID,))

    avgAcoustic = 0.0
    avgDance = 0.0
    avgEnergy = 0.0
    avgInstrument = 0.0
    avgLive = 0.0
    avgSpeech = 0.0
    avgValence = 0.0
    avgTempo = 0.0
    
    isIn = False
    for agg in cursor:
        if agg[0] != None:
            isIn = True
        avgAcoustic = agg[0]
        avgDance = agg[1]
        avgEnergy = agg[2]
        avgInstrument = agg[3]
        avgLive = agg[4]
        avgSpeech = agg[5]
        avgValence = agg[6]
        avgTempo = agg[7]

    if isIn is False:
        return

    artist_query = ("SELECT DISTINCT ArtistID, Genre "
            "FROM UsersFavoriteSongs NATURAL JOIN SpotifyArtist")

    cursor.execute(artist_query, ())

    genre_list = []
    artist_list = []
    for art in cursor:
        artist_list.append(art[0])
        if art[1] not in genre_list:
            genre_list.append(art[1])

    song_query = ("SELECT * FROM SpotifySong NATURAL JOIN SpotifyArtist")

    cursor.execute(song_query, ())
    
    song_heap = []

    for song in cursor:
        total = 0.0
        total += abs(avgAcoustic - song[3])
        total += abs(avgDance - song[4])
        total += abs(avgEnergy - song[5])
        total += abs(avgInstrument - song[6])
        total += abs(avgLive - song[7])
        total += abs(avgSpeech - song[8])
        total += abs(avgValence - song[9])
        total += abs(avgTempo - song[10])
        if song[0] in artist_list:
            total = total * .75
        if song[12] in genre_list:
            total = total * .5
        heapq.heappush(song_heap, (total, song[1], song[2], song[11], song[12]))
    song_list = []
    for i in range(numSongs):
        if len(song_heap) == 0:
            break
        num, songID, name, uri, artist_name = heapq.heappop(song_heap)
        song_list.append((songID, name, artist_name, uri))


    db.commit()
    cursor.close()
    db.close()
# returns a list of tuples (song ID, song name, artist name)
    return song_list 

#insert_user_favorite_songs('test','test',[('songID', 'songName', 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 'sad', 'artistID', 'ArtistName')])
#build_friends_recommended_playlist('test',1)
#delete_user('test')

#get top songs in common
def sharedTopSongs(user1, user2):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()
    query = ("SELECT DISTINCT SpotifySong.SongName, SpotifyArtist.ArtistName"
        "FROM UsersFavoriteSongs AS u1 JOIN UsersFavoriteSongs AS u2 ON (u1.UserID <> u2.UserID and u1.SongID = u2.SongID) JOIN SpotifySong"
        "JOIN SpotifyArtist ON (SpotifyArtist.ArtistID = SpotifySong.ArtistID)"
        "WHERE SpotifySong.SongID = u1.SongID AND u1.UserID LIKE " +str(user1)+" AND u2.UserID LIKE "+str(user2)+"")
    cursor.execute(query, ())

#get average of preferences for user
def getAveragePrefs(userID):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    # retrive avg values for every song's float parameters
    agg_query = ("SELECT AVG(Acousticness), AVG(Danceability), AVG(Energy), AVG(Instrumentalness),"
    " AVG(Liveness), AVG(Speechiness), AVG(Valence), AVG(Tempo)" 
    " FROM UsersFavoriteSongs NATURAL JOIN SpotifySong"
    " WHERE UserID LIKE %s")
    cursor.execute(agg_query, (userID,))
    averages = []
    for agg in cursor:
        print("AGGREGATED IS: " + str(agg))
        averages.append(agg[0])
        averages.append(agg[1])
        averages.append(agg[2])
        averages.append(agg[3])
        averages.append(agg[4])
        averages.append(agg[5])
        averages.append(agg[6])
        averages.append(agg[7])
    db.commit()
    cursor.close()
    db.close()

    return averages
    
def makePlaylistGivenAvg(avg):
    db = pymysql.connect(host='127.0.0.1',database='Music',user='root',password='eiHY?srFG70V') 
    cursor = db.cursor()

    artist_query = ("SELECT DISTINCT ArtistID, Genre "
            "FROM UsersFavoriteSongs NATURAL JOIN SpotifyArtist")

    cursor.execute(artist_query, ())

    genre_list = []
    artist_list = []
    for art in cursor:
        artist_list.append(art[0])
        if art[1] not in genre_list:
            genre_list.append(art[1])
    
    song_query = ("SELECT * FROM SpotifySong NATURAL JOIN SpotifyArtist")

    cursor.execute(song_query, ())
    song_heap = []
    for song in cursor:
        total = 0.0
        total += abs(avg[0] - song[3])
        total += abs(avg[1] - song[4])
        total += abs(avg[2] - song[5])
        total += abs(avg[3] - song[6])
        total += abs(avg[4] - song[7])
        total += abs(avg[5] - song[8])
        total += abs(avg[6]- song[9])
        total += abs(avg[7] - song[10])
        if song[0] in artist_list:
            total = total * .75
        if song[12] in genre_list:
            total = total * .5
        heapq.heappush(song_heap, (total, song[1], song[2], song[11], song[12]))
    song_list = []
    for i in range(25):
        if len(song_heap) == 0:
            break
        num, songID, name, uri, artist_name = heapq.heappop(song_heap)
        song_list.append((songID, name, artist_name, uri))
    db.commit()
    cursor.close()
    db.close()
    return song_list
