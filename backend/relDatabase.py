from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "filip<3ricky"))

def createFriendship(id1, id2):
    with driver.session() as session:
        session.write_transaction(createFriendOf, id1, id2)

def createFriendOf(tx, id1, id2):
    query = (
            "MERGE (u:User { spotifyID: $id1 }) "
            )
    tx.run(query, id1=id1)
    
    query = (
            "MERGE (u:User { spotifyID: $id2 }) "
            )
    tx.run(query, id2=id2)
    
    query = (
            "MATCH (a:User), (b:User) "
            "WHERE a.spotifyID = $id1 and b.spotifyID = $id2 "
            "MERGE (a)-[:FRIENDS]->(b) "
            )
    tx.run(query, id1=id1, id2=id2)

def findFriends(id1):
    with driver.session() as session:
        result = session.write_transaction(findFriendsOf, id1)
        return result
            
def findFriendsOf(tx, id1):
    query = (
            "MATCH (a:User)-[:FRIENDS]->(b:User) "
            "WHERE a.spotifyID = $id1 "
            "RETURN b.spotifyID as ID "
            )
    result = tx.run(query, id1=id1)
    friends = []
    for record in result:
        friends.append(record["ID"])
    return friends

def createListen(id1, id2):
    with driver.session() as session:
        session.write_transaction(createListensTo, id1, id2)

def createListensTo(tx, id1, id2):
    query = (
            "MERGE (u:User { spotifyID: $id1 }) "
            )
    tx.run(query, id1=id1)

    query = (
            "MERGE (a:Artist { artistID: $id2 }) "
            )

    tx.run(query, id2=id2)

    query = (
            "MATCH (u:User), (a:Artist) "
            "WHERE u.spotifyID = $id1 and a.artistID = $id2 "
            "MERGE (u)-[:LISTENS]->(a) "
            )
    tx.run(query, id1=id1, id2 = id2)

def findArtists(id1):
    with driver.session() as session:
        result = session.write_transaction(findArtistsOf, id1)
        return result

def findArtistsOf(tx, id1):
    query = (
            "MATCH (u:User)-[:LISTENS]->(a:Artist) "
            "WHERE u.spotifyID = $id1 "
            "RETURN a.artistID as Artist "
            )
    result = tx.run(query, id1=id1)
    artists = []
    for record in result:
        artists.append(record["Artist"])
    return artists

def deleteUser(id1):
    with driver.session() as session:
        session.write_transaction(deleteUserFrom, id1)
    

def deleteUserFrom(tx, id1):
    query = (
            "MATCH (u:User) "
            "WHERE u.spotifyID = $id1 "
            "DETACH DELETE u "
            )
    tx.run(query, id1=id1)

def insertGenres(id1, genres):
    with driver.session() as session:
        session.write_transaction(insertGenresTo, id1, genres)

def insertGenresTo(tx, id1, genres):
    query = (
            "MERGE  (u:User {spotifyID: $id1 }) "
            )
    tx.run(query, id1= id1)

    for i in range(len(genres)):
        genre = genres[i]
        query = (
                "MERGE (g:Genre {name: $genre }) "
                )
        tx.run(query, genre = genre)

        query = (
                "MATCH (u:User {spotifyID: $id1 }), (g:Genre {name: $genre }) "
                "MERGE (u)-[l:LIKES]->(g) "
                "ON CREATE SET l.weight = 1 "
                "ON MATCH SET l.weight = l.weight + 1 "
                )
        tx.run(query, id1=id1, genre=genre)

def findTotalLikes(id1):
    with driver.session() as session:
        result = session.write_transaction(findTotalLikesOf, id1)
        return result

def findTotalLikesOf(tx, id1):
    query = (
            "MATCH (u:User)-[l:LIKES]->(g:Genre) "
            "WHERE u.spotifyID = $id1 "
            "RETURN g.name as Name, l.weight as Weight "
    )
    result = tx.run(query, id1=id1)
    genres = []
    genreDict = {}
    for record in result:
        thisTuple = (record["Name"], float(record["Weight"]))
        # print(thisTuple)
        genres.append(thisTuple)
    for g in genres:
        genreDict[g[0]] = g[1]
    return genreDict

def findLikes(id1):
    with driver.session() as session:
        result = session.write_transaction(findLikesOf, id1)
        return result

def findLikesOf(tx, id1):
    query = (
            "MATCH (u:User)-[l:LIKES]->(g:Genre) "
            "WHERE u.spotifyID = $id1 "
            "RETURN g.name as Name, l.weight as Weight "
    )
    result = tx.run(query, id1=id1)
    genres = []
    genreDict = {}
    total = 0
    for record in result:
        total += record['Weight']
        thisTuple = (record["Name"], float(record["Weight"]))
        # print(thisTuple)
        genres.append(thisTuple)
    for g in genres:
        percentage = g[1] / total
        genreDict[g[0]] = percentage
    return genreDict

def insertShows(id1, shows):
    with driver.session() as session:
        session.write_transaction(insertShowsTo, id1, shows)

def insertShowsTo(tx, id1, shows):
    #print("inserting to neo4j")
    query = (
            "MERGE (u:User {spotifyID: $id1 }) "
            )
    tx.run(query, id1=id1)
    for i in range(len(shows)):
        #print("forloop")
        id2 = shows[i]
        query = (
                "MERGE (s:Show {showID: $id2 }) "
                )

        tx.run(query, id2=id2)
        query = (
                "MATCH (u:User), (s:Show) "
                "WHERE u.spotifyID = $id1 and s.showID = $id2 "
                "MERGE (u)-[:PODCAST]->(s) "
                )
        tx.run(query, id1=id1, id2=id2)

def findShows(id1):
    with driver.session() as session:
        result = session.write_transaction(findShowsOf, id1)
        return result

def findShowsOf(tx, id1):
    query = (
            "MATCH (u:User)-[:PODCAST]->(s:Show) "
            "WHERE u.spotifyID = $id1 "
            "RETURN s.showID as Show "
            )
    result = tx.run(query, id1=id1)
    
    shows = []
    for record in result:
        shows.append(record["Show"])
    return shows

def findShowListeners(showID):
    with driver.session() as session:
        result = session.write_transaction(findShowListenersOf, showID)
        return result

def findShowListenersOf(tx, showID):
    query = (
        "MATCH (u:User)-[:PODCAST]->(s:Show) "
        "WHERE s.showID = $showID "
        "RETURN (u.SpotifyID)"
    )
    result = tx.run(query, showID=showID)
    listeners = []
    for l in result:
        listeners.append(l)
    return listeners

def insertShowGenres(showID, genres):
    with driver.session() as session:
        session.write_transaction(insertShowGenresTo, showID, genres)

def insertShowGenresTo(tx, showID, genres):
    query = (
            "MERGE (s:Show {showID: $id1 }) "
            )
    tx.run(query, id1= showID)
    for i in range(len(genres)):
        genre = genres[i]
        query = (
                "MERGE (g:Genre {name: $genre }) "
                )
        tx.run(query, genre=genre)

        query = (
                "MATCH (s:Show {showID: $showID }), (g:Genre {name: $genre }) "
                "MERGE (s)-[l:LIKES]->(g) "
                "ON CREATE SET l.weight = 1 "
                "ON MATCH SET l.weight = l.weight + 1 "
                )
        tx.run(query, genre=genre, showID=showID)
        #print("after query", i)


def findShowLikes(showID):
    with driver.session() as session:
        result = session.write_transaction(findLikesOf, showID)
        return result

def findShowLikesOf(tx, showID):
    query = (
            "MATCH (s:Show)-[l:LIKES]->(g:Genre) "
            "WHERE s.showID = $showID "
            "RETURN g.name as Name, l.weight as Weight "
            )
    result = tx.run(query, showID=showID)
    
    genres = []
    genreDict = {}
    total = 0
    for record in result:
        total += record["Weight"]
        thisTuple = (record["Name"], float(record["Weight"]))
        # print(thisTuple)
    for g in genres:
        percentage = g[1] / total
        genreDict[g[0]] = percentage
    return genreDict


#genres = ["rock", "rock", "pop", "rock", "edm"]
#insertGenres("12", genres)
#insertGenres("13", genres)
#insertShows("12", ['joe'])
#insertShows("13",['joe'])

# insertShowGenres("12", ['pop', 'pop','rock'], [1.0,2.0,2.0])
#createFriendship("12", "13", )
#createFriendship("12", "14")
#createFriendship("12", "15")
#result = findFriends("12")
#for friend in result:
#    print(friend)
#createListen("12", "the strokes")
#createListen("12", "flume")
#result= findArtists("12")
#for artist in result:
#    print(artist)
#deleteUser("12")
#deleteUser("13")
#deleteUser("14")
#:deleteUser("15")
#genres = ["rock", "rock", "pop", "rock", "edm"]
#insertGenres("12", genres)
#result = findLikes("12")
#for genre in result:
#    print(result)
#shows = ["Cumtown", "podcast on politics", "podcast3"]
#shows2 = ["podcast4", "podcast on anime girls"]
#insertShows("12", shows)
#insertShows("13", shows2)
#result = findShows("12")
#for show in result:
#    print(show)
#result2 = findShows("13")
#for show2 in result2:
#    print(show2)
