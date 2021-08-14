import React from 'react';
import { BrowserRouter, Route, Switch } from "react-router-dom";
import MainPage from './components/MainPage/MainPage';
import Navbar from './components/Navbar/Navbar';
import Footer from './components/Footer/Footer';
import Squat from './components/TrainingPage/Squat/Squat';

function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <div style={{paddingTop: '50px'}}>
        <Switch>
          <Route exact path="/" component={MainPage} />
          <Route exact path="/squat" component={Squat} />
        </Switch>
      </div>
      <Footer />
    </BrowserRouter>
  );
}

export default App;