<template>
  <div id="app">
    <Menu/>
  </div>
</template>

<script>
import Menu from './components/Menu'
export default {
  name: 'app',
  components: {
    Menu
  },
  data () {
  }
}
</script>

<style>
.el-row {
  margin-bottom: 20px;
}
.el-row:last-child {
  margin-bottom: 0;
}
.el-col {
  border-radius: 4px;
}
  /* #Menu{
    float: top;
  }
  .datas{
    float: top;
    margin-left: 20px;
  } */
</style>
