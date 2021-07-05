import { HashRouter as Router, Switch, Route } from 'react-router-dom';
import SignUp from './pages/Signup';
import Login from './pages/Login';
import MainPage from './pages/MainPage'

function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={MainPage} />
        <Route exact path="/login" component={Login}/>
        <Route exact path="/signup" component={SignUp}/>
      </Switch>
    </Router>
  );
}

export default App;