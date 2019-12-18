import React from 'react';

import { Container, Segment, Table } from 'semantic-ui-react'

import './App.css';

function App() {
  return (
    <Container>
      <Segment>
        CONTROLS
      </Segment>
      <Segment>
        <Table>
          <Table.Header>
            <Table.Row>
              <Table.HeaderCell rowSpan='2'>Job</Table.HeaderCell>
              <Table.HeaderCell rowSpan='2'>Dataset</Table.HeaderCell>
              <Table.HeaderCell rowSpan='2'>Next Run</Table.HeaderCell>
              <Table.HeaderCell colSpan='3'>Status</Table.HeaderCell>
            </Table.Row>
            <Table.Row>
              <Table.HeaderCell>Extract</Table.HeaderCell>
              <Table.HeaderCell>Load</Table.HeaderCell>
              <Table.HeaderCell>Transform</Table.HeaderCell>
            </Table.Row>
          </Table.Header>
          <Table.Body>
          </Table.Body>
        </Table>
      </Segment>
    </Container>
  );
}

export default App;
