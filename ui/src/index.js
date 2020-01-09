import React from 'react';
import ReactDOM from 'react-dom';

import * as serviceWorker from './serviceWorker';

import 'semantic-ui-css/semantic.min.css';
import './index.css';

import { Route, Link, BrowserRouter as Router, Switch } from 'react-router-dom';
import { Menu } from 'semantic-ui-react';

import App from './App';
import Job from './Job';
import NotFound from './404';

const routing = (
  <Router>
    <div>
      <Menu>
        <Menu.Item>
          ICON
        </Menu.Item>
        <Menu.Item header>
          <Link to="/">Home</Link>
        </Menu.Item>
      </Menu>
      <Switch>
        <Route exact path="/" component={App} />
        <Route path="/job/:id?" component={Job} />
        <Route component={NotFound} />
      </Switch>
    </div>
  </Router>
)

ReactDOM.render(routing, document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
