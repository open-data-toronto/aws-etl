<template>
  <sui-table-row>
    <sui-table-cell collapsing>
      {{job}}
    </sui-table-cell>
    <sui-table-cell collapsing>
      WIP
    </sui-table-cell>
    <sui-table-cell collapsing>
      {{job}}
    </sui-table-cell>
    <sui-table-cell collapsing>
      {{job}}
    </sui-table-cell>
    <sui-table-cell collapsing>
      2 Buttons goes here
    </sui-table-cell>
  </sui-table-row>
</template>

<script>
export default {
  name: 'JobStatus',
  props: {
    job: String
  }
}
</script>
