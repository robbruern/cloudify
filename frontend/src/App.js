//import logo from './logo.svg';
import './App.css';
import { useState, useEffect } from 'react'
//import { SpotifyApiContext } from 'react-spotify-api'
import Cookies from 'js-cookie'
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import 'react-spotify-auth/dist/index.css'
import { Container, Row, Col, Button, Card, Cart, Jumbotron } from 'react-bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'

const axios = require('axios');
var ReactDOM = require('react-dom');

let friends = [];
let globalName = "NAME";
let loadedSongs = false;

function App() {
  const [isLoading, setLoading] = useState(true);
  const [users, setUsers] = useState();
  const [name, setName] = useState();
  const [uid, setUid] = useState();
  const [token, setToken] = useState();
  

  document.body.style.background = "#352F2E";
  document.body.style.boxShadow = "inset 0 0 100px rgba(0, 0, 0, .5)";
  // load token from cookies, if previously saved
  // let token = Cookies.get("spotifyAuthToken");

  useEffect(() => {
    if (!token) return;
    if(loadedSongs == false)
    getActiveUsers(token).then(function(result){
      if(result[0][0] == '')
        setUsers([]);
      else
        setUsers(result[0]);
      if(result[1]){
      console.log(result[1].data);
      var name_uid = result[1].data.split(",");
      setName(name_uid[0]);
      setUid(name_uid[1]);
      globalName = name_uid[0];
      }
      setLoading(false);
    });
  }, [token]);
  // if we don't have the token, render the 
if(!token){	  
    return <div className="login_container">
    <div className="header">
     <h1>Welcome to Cloudify!</h1>
	</div>
    <div className="login_button">
      You must login with Spotify to continue.
      <SpotifyAuth
        redirectUri='http://52.14.205.92:3000/callback'
        clientID='97f09e12e273458e9cc101218963d6c5'
        onAccessToken={(token) => setToken(token)}
        scopes={['user-read-private', 'user-read-email', 'user-top-read', 'user-follow-read', 'user-library-read', 'playlist-modify-public']}
      />
    </div>
   </div>
 
  }
  else {
    // send the token to the backend
    if (isLoading)
    {
      return <div className="app">
              <div className="header">
                <h1>Welcome to Cloudify !</h1>
              </div>
                <Container>
                  <Jumbotron>We are loading your top songs into our database now!</Jumbotron>
                  
                </Container>
              </div>
    }
    friends = users;

    return <div className="app">
        <div id = "root">
        <div className="header">
        <h1>Welcome Back to Cloudify, {name}!</h1>
        </div>
        <Container className="playlist_container">
            <div className="friend-header">
                <h1>Recommended by us</h1>
            </div>
            <Row className="playlist_row">
                <Button variant="success" onClick={()=>userLibraryPlaylist(uid, token)}>Create Playlist From All Your Friends</Button>
                {/* <Button variant="success" onClick={()=>podcastPage(uid, token)}>Get Recommended Podcasts</Button> */}
            </Row>
        </Container>
        <Container>
            <Jumbotron>Hit “Create Playlist” over a friends name to dynamically generate a playlist based on their song interests</Jumbotron>
            <Container className="friends">
                <div className="friend-header">
                    <h2>Pick one of your friends on Cloudify to make a custom playlist with:</h2>
                </div>
                <Row className="text-center">
                 
                {users.map((friend) => {
                var user = friend.split(";");
                var userName = user[1];
                var userID = user[0];
                if(userName != name)
                return<Col>
                <Card className="friend">
                    <Card.Body>
                    <Card.Title>
                        Friend
                    </Card.Title>
                    <Card.Text>
                        {userName}
                    </Card.Text>
                    <Button variant="success" onClick={()=>playlistPage(uid, userID, userName, token)}>Create Playlist</Button>
                    </Card.Body>
                </Card>
                </Col>
                })}
                </Row>
            </Container>
        </Container>
        <div>
            <Button className = "deleteButt" variant="danger" onClick={()=>deleteAccount(token)}>Delete Your Information</Button>
        </div>
    </div>
  </div>

  }
}

async function playlistPage(userID, friendID, friendName, token){
  
  var response = await createPlaylist(userID, friendID);
  const data = response.data;
  const songList = data.split(";");
  var uriList = [];
  var basePlaylist = "Playlist with ";
  var name = basePlaylist.concat(friendName);
  ReactDOM.render(
  <div className="app">
    <div id = "root">
      <div className="playlistpage">
    <div className="header">
                <h1>Your custom playlist with {friendName}!</h1>
              </div>
    <Container>
    <Jumbotron>Here is the song list we generated!<br></br> Press the AddToSpotify Button to add the playlist to your account.
    </Jumbotron>
    <div className = "homeButton">
      <Button variant="success" onClick={() => returnHome(token, userID)}>Home</Button>
    </div>
    <div className = "AddPlaylist">
       <Button variant="success" onClick={() => addPlaylist(token, uriList, name)}>AddToSpotify</Button> 
    </div>
    <Container className="friends">
        <div className="friend-header">
          <h2>The songlist:</h2>
        </div>
      {songList.map((song) => {
      var songArtist = song.split("` ");
      uriList.push(songArtist[2]);
      return<Card className="song-card">
        <Card.Body>
          <Card.Title>
            Song: {songArtist[0]}
          </Card.Title>
          <Card.Text>
            Artist: {songArtist[1]}
          </Card.Text>
        </Card.Body>
      </Card>
      })}
    </Container>
  </Container>
  </div>
  </div>
      </div>, document.getElementById('root'))

}
async function podcastPage(userID, token){
  var response = await getPodcasts(userID);
  console.log(response);
  var podcasts = response.data.split("`");
  ReactDOM.render(
  <div className="app">
    <div id = "root">
      <div className="playlistpage">
    <div className="header">
                <h1>Your Recommended Podcasts!</h1>
              </div>
    <Container>
    <Jumbotron>Here is the podlist we generated!
    </Jumbotron>
    <div className = "homeButton">
      <Button variant="success" onClick={() => returnHome(token, userID)}>Home</Button>
    </div>
    <Container className="friends">
        <div className="friend-header">
          <h2>The podlist:</h2>
        </div>
    {podcasts.map((pod) => {
      return<Card className="song-card">
        <Card.Body>
          <Card.Title>
            Podcast: {pod}
          </Card.Title>
        </Card.Body>
      </Card>
      })}
    </Container>
  </Container>
  </div>
  </div>
      </div>, document.getElementById('root'))

}
function returnHome(token, uid){
  ReactDOM.render(
  <div className="app">
      <div id = "root">
      <div className="header">
        <h1>Welcome Back to Cloudify {globalName}!</h1>
      </div>
  <Container>
    
    <Container className="playlist_container">
            <div className="friend-header">
                <h1>Recommended by us</h1>
            </div>
            <Row className="playlist_row">
                <Button variant="success" onClick={()=>userLibraryPlaylist(uid, token)}>Create Playlist From All Your Friends</Button>
                {/* <Button variant="success" onClick={()=>podcastPage(uid, token)}>Get Recommended Podcasts</Button> */}
            </Row>
        </Container>
        <Jumbotron>Hit “Create Playlist” over a friends name to dynamically generate a playlist based on their song interests</Jumbotron>
    <Container className="friends">
        <div className="friend-header">
          <h2>Pick one of your friends to make a custom playlist with:</h2>
        </div>
      <Row className="text-center">
      {friends.map((friend) => {
      var user = friend.split(";");
      var userName = user[1];
      var userID = user[0];
      if(userName != globalName)
      return<Col>
      <Card className="friend">
        <Card.Body>
          <Card.Title>
            Friend
          </Card.Title>
          <Card.Text>
            {userName}
          </Card.Text>
          <Button variant="success" onClick={()=>playlistPage(uid, userID, userName, token)}>Create Playlist</Button>
        </Card.Body>
      </Card>
      </Col>
      })}
      </Row>
    </Container>
  </Container>
      <div>
          <Button className = "deleteButt" variant="danger" onClick={()=>deleteAccount(token)}>Delete Your Information</Button>
      </div>
  </div>
  </div>, document.getElementById('root'))
}

async function userLibraryPlaylist(userID, token){
  
  var response = await createAllPlaylist(token);
  const data = response.data;
  const songList = data.split(";");
  var uriList = [];
  var name = "Custom Individual Playlist";
  ReactDOM.render(
  <div className="app">
    <div id = "root">
      <div className="playlistpage">
    <div className="header">
                <h1>Your All Friends custom playlist!</h1>
              </div>
    <Container>
    <Jumbotron>Here is the song list we generated!<br></br> Press the AddToSpotify Button to add the playlist to your account.
    </Jumbotron>
    <div className = "homeButton">
      <Button variant="success" onClick={() => returnHome(token, userID)}>Home</Button>
    </div>
    <div className = "AddPlaylist">
       <Button variant="success" onClick={() => addAllPlaylist(token, uriList, name)}>AddToSpotify</Button> 
    </div>
    <Container className="friends">
        <div className="friend-header">
          <h2>The songlist:</h2>
        </div>
      {songList.map((song) => {
      var songArtist = song.split("` ");
      uriList.push(songArtist[2]);
      return<Card className="song-card">
        <Card.Body>
          <Card.Title>
            Song: {songArtist[0]}
          </Card.Title>
          <Card.Text>
            Artist: {songArtist[1]}
          </Card.Text>
        </Card.Body>
      </Card>
      })}
    </Container>
  </Container>
  </div>
  </div>
      </div>, document.getElementById('root'))

}

async function sendToken(token){
  return await axios.post('http://52.14.205.92:5000/token', {token: token})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function createPlaylist(userID, friendID, name){
  return await axios.post('http://52.14.205.92:5000/createFriendPlaylist', {userID: userID, friendID: friendID, name: name})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function createAllPlaylist(token){
  return await axios.post('http://52.14.205.92:5000/createAllFollowingPlaylist', {token : token})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function getPodcasts(uid){
  return await axios.post('http://52.14.205.92:5000/getRecommendedPodcasts', {uid: uid})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function getActiveUsers(token){
  var name_uid = await sendToken(token);
  var uid = "";
  if(name_uid)
  uid = name_uid.data.split(",")[1];
  const response = await axios.post('http://52.14.205.92:5000/activeUsers', {uid: uid});
  console.log(response.data);
  return [response.data.split(","), name_uid];
}

async function deleteAccount(token) {
    return await axios.post('http://52.14.205.92:5000/deleteUser', {token: token})
      .then(function (response) {
        alert("You're account has been removed from our database!");
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function addPlaylist(token, songUriList, name) {
    return await axios.post('http://52.14.205.92:5000/addPlaylistToLibrary', {token: token, uris: songUriList, name: name})
      .then(function (response) {
        alert("You're playlist has been created!");
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function addAllPlaylist(token, songUriList, name) {
  return await axios.post('http://52.14.205.92:5000/addAllFollowingPlaylist', {token: token, uris: songUriList, name: name})
    .then(function (response) {
      alert("You're playlist has been created!");
      console.log(response);
      return response;
    })
    .catch(function (error) {
      console.log(error);
    });
}

export default App;
