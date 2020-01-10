import React from 'react';
import update from 'immutability-helper';

import axios from 'axios';

import { Button, Checkbox, Container, Icon, Segment, Table } from 'semantic-ui-react'

import './App.css';

class App extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'rules': []
    }

    this.list();
  }

  list = async () => {
    await axios.get(
      process.env.REACT_APP_JOB_SHOW
    ).then(response => {
      const
        data = response.data.Rules,
        rules = data.map((r) => {
          return {
            name: r.Name,
            arn: r.Arn,
            schedule: r.ScheduleExpression,
            isEnabled: r.State === 'ENABLED'
          }
        });

      this.setState({ 'rules': rules });

      console.log(this.state)
    }).catch(e => {
      console.log(`ERROR: ${e}`);
    });
  }

  toggleJob = async (event, index, arn) => {
    this.setState({
      'rules': update(
        this.state.rules,
        { [ index ]: { isEnabled : { $set: event.checked } } }
      )
    });
  }

  render() {
    return (
      <Container>
        <Segment>
          <Table striped basic>
            <Table.Header>
              <Table.Row>
                <Table.HeaderCell>Status</Table.HeaderCell>
                <Table.HeaderCell>Name</Table.HeaderCell>
                <Table.HeaderCell>Schedule</Table.HeaderCell>
                <Table.HeaderCell>Last 5 Run Status</Table.HeaderCell>
                <Table.HeaderCell>Next Run</Table.HeaderCell>
                <Table.HeaderCell textAlign='center'>Run Once</Table.HeaderCell>
                <Table.HeaderCell textAlign='center'>Configure</Table.HeaderCell>
                <Table.HeaderCell textAlign='center'>Delete</Table.HeaderCell>
              </Table.Row>
            </Table.Header>

            <Table.Body>
              {
                this.state.rules.map((job, index) => (
                  <Table.Row key={ index }>
                    <Table.Cell collapsing>
                      <Checkbox
                        slider
                        checked={ job.isEnabled }
                        onChange={ (event, result) => this.toggleJob(result, index, job.arn) }
                      />
                    </Table.Cell>
                    <Table.Cell>{ job.name }</Table.Cell>
                    <Table.Cell>{ job.schedule }</Table.Cell>
                    <Table.Cell>WIP</Table.Cell>
                    <Table.Cell>WIP</Table.Cell>
                    <Table.Cell textAlign='center'>
                    <Button icon color='green' onClick={ () => window.location.href = `/job/${job.name}` }><Icon name='shipping fast' /></Button>
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                      <Button icon color='blue' onClick={ () => window.location.href = `/job/${job.name}` }><Icon name='sliders horizontal' /></Button>
                    </Table.Cell>
                    <Table.Cell textAlign='center'>
                      <Button icon color='red'><Icon name='trash' /></Button>
                    </Table.Cell>
                  </Table.Row>
                ))
              }

            </Table.Body>

            <Table.Footer fullWidth>
              <Table.Row>
                <Table.HeaderCell />
                <Table.HeaderCell colSpan='7'>
                  <Button icon labelPosition='left' color='green' onClick={ () => window.location.href = '/job' }>
                    <Icon name='plus' /> Add Job
                  </Button>
                </Table.HeaderCell>
              </Table.Row>
            </Table.Footer>
          </Table>
        </Segment>
      </Container>
    );
  }
}
export default App;
