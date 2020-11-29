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

function App() {
  const [isLoading, setLoading] = useState(true);
  const [users, setUsers] = useState();

  useEffect(() => {
    getActiveUsers(token).then(function(result){
      setUsers(result);
      setLoading(false);
    });
  }, []);

  document.body.style.background = "#352F2E";
  document.body.style.boxShadow = "inset 0 0 100px rgba(0, 0, 0, .5)";
  // load token from cookies, if previously saved
  const token = Cookies.get("spotifyAuthToken");

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
        scopes={[Scopes.userReadPrivate, 'user-read-email']}
      />
    </div>
   </div>
 
  }
  else {
    // send the token to the backend
    if (isLoading){
      return <div className="app">
      <div className="header">
        <h1>Welcome Back to Cloudify NAME !</h1>
      </div>
  <Container>
    <Jumbotron>Info on what you can do with Cloudify</Jumbotron>
    <Container className="friends">
        <div className="friend-header">
          <h2>Pick one of your friends to make a custom playlist with:</h2>
        </div>
      <Row className="text-center">
      {friends.map((friend) => {
      return<Col>
      <Card className="friend">
        <Card.Body>
          <Card.Title>
            Friend
          </Card.Title>
          <Card.Text>
            {friend}
          </Card.Text>
          <Button variant="success" >Create Playlist</Button>
        </Card.Body>
      </Card>
      </Col>
      })}
      </Row>
    </Container>
  </Container>
  </div>

    }
      return <div className="app">
      <div className="header">
        <h1>Welcome Back to Cloudify NAME !</h1>
      </div>
  <Container>
    <Jumbotron>Info on what you can do with Cloudify</Jumbotron>
    <Container className="friends">
        <div className="friend-header">
          <h2>Pick one of your friends to make a custom playlist with:</h2>
        </div>
      <Row className="text-center">
      {users.map((friend) => {
      return<Col>
      <Card className="friend">
        <Card.Body>
          <Card.Title>
            Friend
          </Card.Title>
          <Card.Text>
            {friend}
          </Card.Text>
          <Button variant="success" >Create Playlist</Button>
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
  await axios.post('http://52.14.205.92:5000/token', {token: token})
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
}

async function getActiveUsers(token){
  await sendToken(token);
  const response = await axios.get('http://52.14.205.92:5000/activeUsers');
  return response.data.split(",");
}

export default App;
