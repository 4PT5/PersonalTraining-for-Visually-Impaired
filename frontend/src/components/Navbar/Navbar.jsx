import React, { useState } from 'react'

import { Avatar, Anchor, Nav, Grommet, Header, Button, Icons, Menu} from 'grommet';
import { grommet } from 'grommet/themes';

function Navbar() {
    return (
      <Header background="brand">
        <Button  hoverIndicator />
        <Menu label="account" items={[{ label: 'logout' }]} />
      </Header>
    );
}

export default Navbar