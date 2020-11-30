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

let friends = [];
let name = "NAME";

function App() {
  const [isLoading, setLoading] = useState(true);
  const [isPlayist, setPlaylist] = useState(true);
  const [users, setUsers] = useState();
  const [name, setName] = useState();



  document.body.style.background = "#352F2E";
  document.body.style.boxShadow = "inset 0 0 100px rgba(0, 0, 0, .5)";
  // load token from cookies, if previously saved
  let token = Cookies.get("spotifyAuthToken");

  useEffect(() => {
    getActiveUsers(token).then(function(result){
      setUsers(result[0]);
      if(result[1]){
      console.log(result[1].data);
      setName(result[1].data);
      }
      setLoading(false);
    });
  }, []);
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
        scopes={['user-read-private', 'user-read-email', 'user-top-read', 'user-follow-read']}
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
      return <div className="app">
      <div className="header">
        <h1>Welcome Back to Cloudify {name} !</h1>
      </div>
  <Container>
    <Jumbotron>Hit “Create Playlist” over a friends name to dynamically generate a playlist based on their song interests</Jumbotron>
    <Container className="friends">
        <div className="friend-header">
          <h2>Pick one of your friends to make a custom playlist with:</h2>
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
          <Button variant="success" onClick={()=>createPlaylist(userID)}>Create Playlist</Button>
        </Card.Body>
      </Card>
      </Col>
      })}
      </Row>
    </Container>
  </Container>
  </div>

    console.log("Other one");
    console.log(friends);
    
  }
}

async function sendToken(token){
  console.log(token);
  return await axios.post('http://52.14.205.92:5000/token', {token: token})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function createPlaylist(friendID){
  return await axios.post('http://52.14.205.92:5000/createPlaylist', {friendID: friendID})
      .then(function (response) {
        console.log(response);
        return response;
      })
      .catch(function (error) {
        console.log(error);
      });
}


async function getActiveUsers(token){
  name = await sendToken(token);
  const response = await axios.get('http://52.14.205.92:5000/activeUsers');
  console.log(response.data);
  return [response.data.split(","), name];
}

export default App;
