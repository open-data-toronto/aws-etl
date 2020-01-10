import React from 'react';
import update from 'immutability-helper';

import axios from 'axios';

import { Button, Container, Divider, Form, Header, Input, Message, Segment, Select, TextArea } from 'semantic-ui-react'

// TODO: checkout later.js for cron expression calculation

class Job extends React.Component {
  constructor(props) {
    super(props);

    const { params } = this.props.match;

    this.header = {
      icon: params.id ? 'arrow alternate circle up outline' : 'plus square outline',
      text: params.id ? 'Update existing extract' : 'Configure new extract'
    }

    this.state = {
      id: params.id || '',
      extract: '',
      transform: '',
      load: 'load',
      request: '',
      cron: '',
      fields: [{
        id: '',
        type: '',
        description: '',
        error: false
      }],
      _mode: params.id ? 'update' : 'create',
      _nameError: false,
      _cronError: false,
      _requestError: false,
      _fieldError: false
    }

    this.options = {
      extract: [
        { key: 'arcgis', text: 'ArcGIS', value: 'arcgis' }
      ],
      transform: [
        { key: 'basic', text: 'Basic (field type validation ONLY)', value: 'transform' },
        { key: 'arcgis', text: 'ArcGIS (projection validations)', value: 'arcgis'}
      ],
      fieldTypes: [
        { key: 'bool', text: 'boolean', value: 'bool' },
        { key: 'int', text: 'integer', value: 'int' },
        { key: 'float', text: 'float', value: 'float' },
        { key: 'text', text: 'text', value: 'text' },
        { key: 'timestamp', text: 'timestamp', value: 'timestamp' }
      ]
    }

    if (params.id) {
      this.fetch(params.id);
    }
  }

  dropdownChange = (event, result) => {
    const { name, value } = result || event.target;
    this.setState({ [name]: value });
  }

  addField = (event) => {
    event.preventDefault();

    this.setState({
      fields: this.state.fields.concat([{
        'id': '',
        'type': '',
        'description': ''
      }])
    });
  }

  generateFields = (event) => {
    event.preventDefault();
    // axios fetch source content
  }

  fetch = async (id) => {
    await axios.get(
      process.env.REACT_APP_JOB_SHOW,
      {
        params: {
          id: id
        }
      }
    ).then(response => {
      if (typeof(response.data.request) === 'object') {
        response.data.request = JSON.stringify(response.data.request, null, 2);
      }

      this.setState(response.data);
    })
  }

  submit = async () => {
    const payload = {};

    let pass = true;
    Object.entries(this.state).forEach(([key, value]) => {
      if (key.startsWith('_')) return;

      switch(key) {
        // case 'id':
        //   // call ckan and see if dataset exists
        //
        //   payload[key] = value;
        //   break;
        // case 'cron':
        //   pass &= this.cronRegEx.test(value);
        //   this.setState({ _cronError: true });
        //
        //   payload[key] = value;
        //   break;
        case 'request':
          if (this.state.extract === 'arcgis') {
            try {
              value = JSON.parse(this.state.request);
            } catch {
              pass = false;
              this.setState({ _requestError: false });
            }
          }
          break;
      }

      payload[key] = value;
    });

    if (pass) {
      await axios.post(
        process.env.REACT_APP_JOB_SUBMIT,
        JSON.stringify(payload),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      ).then((response) => {
        window.location.href = '/';
      });
    }
  }

  render() {
    return (
      <Container>
        <Header as='h3' icon={ this.header.icon } content={ this.header.text } />
        <Divider />
        <Form>
          <Form.Field required
            id='form-input-dataset-name'
            name='id'
            control={Input}
            label='Dataset name'
            placeholder='City Wards'
            disabled={ this.state._mode === 'update' }
            value={ this.state.id }
            onChange={ (e) => this.setState({ 'id': e.target.value }) }
          />
          <Form.Group widths='equal'>
            <Form.Field required
              id='form-select-extract-type'
              name='extract'
              control={Select}
              options={this.options.extract}
              label={{ children: 'Source system', htmlFor: 'form-select-extract-type' }}
              placeholder='eg. ArcGIS'
              value={ this.state.extract }
              onChange={ this.dropdownChange }
            />
            <Form.Field required
              id='form-select-transform-type'
              name='transform'
              control={Select}
              options={this.options.transform}
              label={{ children: 'Processing', htmlFor: 'form-select-transform-type' }}
              placeholder='eg. data type validation'
              value={ this.state.transform }
              onChange={ this.dropdownChange }
            />
          </Form.Group>
          <Form.Field required
            id='form-textarea-extract-parameters'
            name='request'
            control={TextArea}
            label='Extract parameters'
            placeholder='eg. SQL query for databases or request parameters for API sources'
            error={ this.state._requestError }
            value={ this.state.request }
            onChange={ this.dropdownChange }
          />
          <Form.Field required
            id='form-input-cron'
            name='cron'
            control={Input}
            label='Cron schedule'
            placeholder='0 0 * * *'
            value={ this.state.cron }
            onChange={ (e) => this.setState({ 'cron': e.target.value }) }
          />
          <Segment>
            <h5>Data dictionary</h5>
            <Message negative header='Invalid field(s) provided' content='please provide both field name and data type' hidden={ !this.state._fieldError }/>
            {
              this.state.fields.map((f, i) => (
                <Form.Group widths='equal' key={ i }>
                  <Form.Field
                    control={ Input }
                    name={ `id-${i}` }
                    placeholder='Field name'
                    value={ f.id }
                    onChange={ (e) =>
                      this.setState({
                        'fields': update(this.state.fields, { [ i ]: { id: { $set: e.target.value } } })
                      })
                    }
                  />
                  <Form.Field
                    control={ Select }
                    name={ `type-${i}` }
                    options={ this.options.fieldTypes }
                    placeholder='Data type'
                    value={ f.type }
                    onChange={ (event, result) =>
                      this.setState({
                        'fields': update(
                          this.state.fields,
                          { [ i ]: { type: { $set: result.value } } }
                        )
                      })
                    }
                  />
                  <Form.Field
                    control={ Input }
                    name={ `description-${i}` }
                    placeholder='Descriptions'
                    value={ f.description }
                    onChange={ (e) =>
                      this.setState({
                        'fields': update(this.state.fields, { [ i ]: { description: { $set: e.target.value } } })
                      })
                    }
                  />
                </Form.Group>
              ))
            }
            <div>
              <Button content='Fetch fields' onClick={ this.generateFields } />
              <Button icon='plus' onClick={ this.addField } />
            </div>
          </Segment>
          <Form.Field control={Button} positive onClick={ () => this.submit() }>Submit</Form.Field>
        </Form>
      </Container>
    );
  }
}

export default Job
