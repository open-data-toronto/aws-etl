import React from 'react'

import { Link } from 'react-router-dom'
import { Menu } from 'semantic-ui-react'

import './NavBar.css'

class NavBar extends React.Component {
  render() {
    return (
      <Menu>
        <Menu.Item>
          ICON
        </Menu.Item>
        <Menu.Item header>
          <Link to="/">Home</Link>
        </Menu.Item>
      </Menu>
    );
  }
}

export default NavBar
