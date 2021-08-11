import React from 'react';
import { Grommet } from 'grommet';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import MainPage from "./components/MainPage/MainPage";
import Navbar from './components/Navbar/Navbar';

function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <div>
        <Switch>
          <Route exact path="/" component={MainPage} />
        </Switch>
      </div>
    </BrowserRouter>
  );
}

export default App;