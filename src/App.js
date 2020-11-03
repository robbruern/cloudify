import React from 'react';
import logo from './logo.svg';
import './App.css';
import Amplify from '@aws-amplify/core';
import API from '@aws-amplify/api';
import Auth from '@aws-amplify/auth';
import awsconfig from 'aws-exports.js';

Amplify.configure(awsconfig);

async function signUp() {
  try {
      const { user } = await Auth.signUp({
          username,
          password,
          attributes: {
              email,          // optional
              phone_number,   // optional - E.164 number convention
              // other custom attributes 
          }
      });
      console.log(user);
  } catch (error) {
      console.log('error signing up:', error);
  }
}

async function confirmSignUp() {
  try {
    await Auth.confirmSignUp(username, code);
  } catch (error) {
      console.log('error confirming sign up', error);
  }
}

async function signIn() {
  try {
      const user = await Auth.signIn(username, password);
  } catch (error) {
      console.log('error signing in', error);
  }
}

async function signOut() {
  try {
      await Auth.signOut();
  } catch (error) {
      console.log('error signing out: ', error);
  }
}

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1>API TESTING IN POGRESS</h1>
      </header>
    </div>
  );
}

export default App;
