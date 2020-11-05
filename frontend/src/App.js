//import logo from './logo.svg';
import './App.css';

//import { SpotifyApiContext } from 'react-spotify-api'
import Cookies from 'js-cookie'
import { SpotifyAuth, Scopes } from 'react-spotify-auth'
import 'react-spotify-auth/dist/index.css'
const axios = require('axios');


function App() {
  document.body.style.background = "#352F2E";
  // load token from cookies, if previously saved
  const token = Cookies.get("spotifyAuthToken");

  // if we don't have the token, render the 
  //if (!token) {
if(1){	  
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
    axios.post('http://52.14.205.92:5000/token', {token: token})
      .then(function (response) {
        console.log(response);
      })
      .catch(function (error) {
        console.log(error);
      });
    return <div className="app">
      <div className="header">
	<h1>Welcom Back to Cloudify!</h1>
      </div>
    </div>
  }
}

export default App;
