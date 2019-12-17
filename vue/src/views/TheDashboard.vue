<template lang='html'>
  <sui-container>
    <!-- TODO: add controls (eg. add new job and stuff) -->

    <sui-grid centered>
      <sui-segment basic centered>
        <sui-table>
          <sui-table-header>
            <sui-table-row>
              <sui-table-header-cell>Job</sui-table-header-cell>
              <sui-table-header-cell>Status</sui-table-header-cell>
              <sui-table-header-cell>Next Run</sui-table-header-cell>
              <sui-table-header-cell>Dataset</sui-table-header-cell>
              <sui-table-header-cell>Controls</sui-table-header-cell>
            </sui-table-row>
          </sui-table-header>
          <sui-table-body>
            <JobStatus v-for="(item, idx) in ['city-ward', 'or something']" :key='idx' :job='item'/>
          </sui-table-body>
        </sui-table>
      </sui-segment>
    </sui-grid>
  </sui-container>
</template>

<script>
import JobStatus from '@/components/JobStatus'

export default {
  name: 'TheDashboard',
  components: {
    JobStatus
  },
  props: {
    // jobs: Array
  }
}
</script>
