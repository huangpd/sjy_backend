<template>
  <div id="menu">
    <!-- <el-radio-group v-model="isCollapse" style="margin-bottom: 20px; ">
      <el-radio-button :label="false">展开</el-radio-button>
      <el-radio-button :label="true">收起</el-radio-button>
      <h3>小镇系统管理</h3>
    </el-radio-group>-->

    <el-row type="flex" justify="start">
      <el-col :span="3">
        <h3>小镇管理系统</h3>
      </el-col>

      <el-col :span="10">
        <el-menu
          :default-active="indexs"
          class="el-menu-demo"
          mode="horizontal"
          @open="handleOpen"
          @close="handleClose"
          router
        >
          <el-menu-item index="/town_home/">
            <i class="el-icon-s-home"></i>
            <span slot="title">小镇仪表</span>
          </el-menu-item>

          <el-menu-item index="/town_enter/">
            <i class="el-icon-menu"></i>
            <span slot="title">小镇录入</span>
          </el-menu-item>

          <el-menu-item index="/town_company/">
            <i class="el-icon-setting"></i>
            <span slot="title">入驻公司录入</span>
          </el-menu-item>
        </el-menu>
      </el-col>
    </el-row>

    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "menu",
  data() {
    return {
      indexs: "",
      isCollapse: true
    };
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
.el-menu {
  float: left;
  z-index: 1;
  margin-right: 20px;
}
.el-radio-group {
  position: inherit;
  margin-top: 0;
  width: 100%;
  z-index: 1;
  font-size: 1.17em;
}
h3 {
  display: inline-block;
  margin-left: 50px;
}
.town_data {
  display: inline;
}
.el-divider {
  margin-top: 0;
}
</style>
