import React from 'react';
import update from 'immutability-helper';

import axios from 'axios';

import { Button, Container, Divider, Form, Header, Input, Message, Segment, Select, TextArea } from 'semantic-ui-react'

//TODO: dropdown requires 2 clicks to change

class Job extends React.Component {
  constructor(props) {
    super(props);

    const { params } = this.props.match;

    this.header = {
      icon: params.id ? 'arrow alternate circle up outline' : 'plus square outline',
      text: params.id ? 'Update existing extract' : 'Configure new extract'
    }

    this.job = params.id;

    this.state = {
      dataset: '',
      extract: '',
      transform: '',
      extractParams: '',
      cron: '',
      fields: [{
        id: '',
        type: '',
        description: '',
        error: false
      }],
      nameError: false,
      extractError: false,
      transformError: false,
      accessError: false,
      fieldError: false
    }

    this.options = {
      extract: [
        { key: 'arcgis', text: 'ArcGIS', value: 'arcgis' }
      ],
      transform: [
        { key: 'basic', text: 'Basic (field type validation ONLY)', value: 'transform' }
      ],
      dataTypes: [
        { key: 'bool', text: 'boolean', value: 'bool' },
        { key: 'int', text: 'integer', value: 'int' },
        { key: 'float', text: 'float', value: 'float' },
        { key: 'text', text: 'text', value: 'text' },
        { key: 'timestamp', text: 'timestamp', value: 'timestamp' }
      ]
    }


  }

  addField = () => {
    this.setState({
      fields: this.state.fields.concat([{
        'id': '',
        'type': '',
        'description': ''
      }])
    });
  }

  generateFields = () => {
    // axios fetch source content
  }

  fetch = () => {
    // axios fetch existing job schedule and config file
  }

  submit = () => {

  }

  render() {
    return (
      <Container>
        <Header as='h3' icon={ this.header.icon } content={ this.header.text } />
        <Divider />
        <Form>
          <Form.Field required
            id='form-input-dataset-name'
            control={Input}
            label='Dataset name'
            placeholder='City Wards'
            value={ this.state.dataset }
            onChange={ (e) => this.setState({ 'dataset': e.target.value }) }
          />
          <Form.Group widths='equal'>
            <Form.Field required
              id='form-select-extract-type'
              control={Select}
              options={this.options.extract}
              label={{ children: 'Source system', htmlFor: 'form-select-extract-type' }}
              placeholder='eg. ArcGIS'
              value={ this.state.extract }
              onChange={ (e) => this.setState({ 'extract': e.target.value }) }
            />
            <Form.Field required
              id='form-select-transform-type'
              control={Select}
              options={this.options.transform}
              label={{ children: 'Processing', htmlFor: 'form-select-transform-type' }}
              placeholder='eg. data type validation'
              value={ this.state.transform }
              onChange={ (e) => this.setState({ 'transform': e.target.value }) }
            />
          </Form.Group>
          <Form.Field required
            id='form-textarea-extract-parameters'
            control={TextArea}
            label='Extract parameters'
            placeholder='eg. SQL query for databases or request parameters for API sources'
            error={ this.state.accessError }
            value={ this.state.extractParams }
            onChange={ (e) => this.setState({ 'extractParams': e.target.value }) }
          />
          <Form.Field required
            id='form-input-cron'
            control={Input}
            label='Cron schedule'
            placeholder='0 0 * * *'
            value={ this.state.cron }
            onChange={ (e) => this.setState({ 'cron': e.target.value }) }
          />
          <Segment>
            <h5>Data dictionary</h5>
            <Message negative header='Invalid field(s) provided' content='please provide both field name and data type' hidden={ !this.state.fieldError }/>
            {
              this.state.fields.map((f, i) => (
                <Form.Group widths='equal' key={ i }>
                  <Form.Field
                    control={Input}
                    placeholder='Field name'
                    value={ f.id }
                    onChange={ (e) =>
                      this.setState({
                        'fields': update(this.state.fields, {[ i ]: {id: {$set: e.target.value}}})
                      })
                    }
                  />
                  <Form.Field
                    control={Select}
                    options={this.options.dataTypes}
                    placeholder='Data type'
                    value={ f.type }
                    onChange={ (e) =>
                      this.setState({
                        'fields': update(this.state.fields, {[ i ]: {type: {$set: e.target.value}}})
                      })
                    }
                  />
                  <Form.Field
                    control={Input}
                    placeholder='Descriptions'
                    value={ f.description }
                    onChange={ (e) =>
                      this.setState({
                        'fields': update(this.state.fields, {[ i ]: {description: {$set: e.target.value}}})
                      })
                    }
                  />
                </Form.Group>
              ))
            }
            <div>
              <Button content='Fetch fields' onClick={ () => this.generateFields() } />
              <Button icon='plus' onClick={ () => this.addField() } />
            </div>
          </Segment>
          <Form.Field control={Button} positive onClick={ () => this.submit() }>Submit</Form.Field>
        </Form>
      </Container>
    )
  }
}

export default Job
