import React from "react";
import { HashRouter as Router, Switch, Route } from "react-router-dom";
import SignUp from "./pages/Signup";
import Login from "./pages/Login";
import MainPage from "./pages/MainPage";
import axios from "axios";

axios.defaults.withCredentials = true;

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={MainPage} />
        <Route exact path="/login" component={Login} />
        <Route exact path="/signup" component={SignUp} />
      </Switch>
    </Router>
  );
}

export default App;
